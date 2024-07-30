from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from julia.api import Julia
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# transfer the variables into python

app = Flask(__name__)
app.secret_key = "hello"

jl = Julia(compiled_modules=False)

jl.eval("using CSV")
jl.eval("using DataFrames")
jl.eval("using QuartetNetworkGoodnessFit")
jl.eval("using PhyloNetworks")
###################### home page #######################
@app.route("/")
def home():
    return render_template('home.html')

###################### file upload #####################
UPLOAD_FOLDER = './upload_data'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'rtf', 'tre'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No file part", "info")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash("No selected file", "info")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Successfully uploaded!", "info")
            return redirect(url_for('home'))
    return render_template("data_upload.html")

######################### clustering ######################
@app.route("/clustering")
def clustering():
    return "This is the clustering page."

######################## goodness of fit #####################
if not os.path.exists('plots'):
    os.makedirs('plots')

@app.route("/goodness", methods = ['GET', 'POST'])
def goodness(): 
    plot_url = None
    if request.method == 'POST':
        optimal_bl = request.form['optbl']
        test_stat = request.form['test_stat']
        correct = request.form['corr']
        set_seed = request.form['seed']
        num_sim = request.form['nsim']
        diagnose = request.form['diag']
        keep = request.form['save']
        
        gene = jl.eval('joinpath("uploud_data/gene_tree.rtf")')
        readmultopo = jl.eval("readMultiTopology")
        genetrees = readmultopo(gene)
        countquartetsintrees = jl.eval('countquartetsintrees')
        q,t = countquartetsintrees(genetrees)
        writeTableCF = jl.eval('writeTableCF')
        df = writeTableCF(q,t) # make a table with the 4-taxa and its CF
        # this df if what we can pass to the Goodness-of-fit function

        # we can write that into a csv file for later usage
        CSVwrite = jl.eval('CSV.write')
        CSVwrite("tableCF.csv", df)
        readTableCF = jl.eval('readTableCF')
        geneCF = readTableCF("tableCF.csv")
        readTopology = jl.eval('readTopology')
        species_tree = readTopology("(Smi165:18.12505298,(Age001:8.747492442,(Adi001:8.308140028,(((Asu001:3.171531094,Aga001:3.171531094):2.767496398,(Ape001:1.381629136,(Aza037:1.363263922,Ama006:1.363263922):0.01836521346):4.555985647):0.1963665132,Aru001:6.135394005):2.172746023):0.4393524143):9.377560535);")

        quarnetGoFtest = jl.eval('quarnetGoFtest!')
        res = quarnetGoFtest(species_tree, geneCF, optimal_bl, test_stat, correct,
                                set_seed, num_sim, diagnose, keep)
        overall_p = res[1]
        uncorrected_z = res[2]
        sigma = res[3]
        pval_vec = res[4]
        optnet = res[5]
        z_vec = res[6]
        count = 0
        for z in z_vec:
            if z > uncorrected_z:
                count += 1
            elif z == uncorrected_z:
                count += 1
        prop_greater = count / len(z_vec)

        try:
            plt.figure()
            plt.hist(pval_vec)
            # save plot
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close()
        except ValueError:
            plot_url = None
    return render_template("goodness.html", plot_url = plot_url)

'''# read parameters from users
@app.route("/process", method = ['GET'])
def process():
    
    return render_template("goodness_submit.html")'''




'''
@app.route("/plot")
def goodness_plot():
    gene = jl.eval('joinpath("uploud_data/gene_tree.rtf")')
    readmultopo = jl.eval("readMultiTopology")
    genetrees = readmultopo(gene)
    countquartetsintrees = jl.eval('countquartetsintrees')
    q,t = countquartetsintrees(genetrees)
    writeTableCF = jl.eval('writeTableCF')
    df = writeTableCF(q,t) # make a table with the 4-taxa and its CF
    # this df if what we can pass to the Goodness-of-fit function

    # we can write that into a csv file for later usage
    CSVwrite = jl.eval('CSV.write')
    CSVwrite("tableCF.csv", df)
    readTableCF = jl.eval('readTableCF')
    geneCF = readTableCF("tableCF.csv")

    readTopology = jl.eval('readTopology')
    species_tree = readTopology("(Smi165:18.12505298,(Age001:8.747492442,(Adi001:8.308140028,(((Asu001:3.171531094,Aga001:3.171531094):2.767496398,(Ape001:1.381629136,(Aza037:1.363263922,Ama006:1.363263922):0.01836521346):4.555985647):0.1963665132,Aru001:6.135394005):2.172746023):0.4393524143):9.377560535);")

    topologyMaxQPseudolik = jl.eval('topologyMaxQPseudolik!')
    topologyMaxQPseudolik(species_tree, geneCF)
    fittedQuartetCF = jl.eval('fittedQuartetCF')
    # df_long = fittedQuartetCF(geneCF, :long)
    # scatter plot

    # plot(df_long[""])
    # return render_template('goodness.html', name = plt.show())
'''
    
# create global variables in order to get value and use them in different functions
'''optimal_bl = None
test_stat = None
correct = None
set_seed = None
num_sim = None
diagnose = None
keep = None'''
# define a route to handle the parameters



if __name__ == "__main__":
    app.run(debug = True)
