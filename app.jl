using PhyloClustering, PhyloNetworks, CSV, DataFrames
using MLJ

using GenieFramework
@genietools

algorithms = [:YinyangKmeans, :GaussianMixture, :Hierarchical, :DBSCAN]
PCA = @load PCA pkg = "MultivariateStats"

function convertPCA(trees)
    model = PCA(maxoutdim=2)
    mach = machine(model, trees) |> fit!
    trees_PCA = MLJ.transform(mach, trees)
    return trees_PCA
end

# TODO different clusteirng algorithms have different Parameters
# TODO file uploader; Refresh button
@handlers begin
    @in num_of_clusters = 2
    @in algorithm = :YinyangKmeans
    # @in num_of_taxa = 4
    # @in trees = readMultiTopology("data/4_diff_topo_1_50_1.trees")
    @in trees = CSV.read("data/4_diff_topo_1_50_1.csv", DataFrame)
    @out datatable = DataTable()
    @out datatablepagination = DataTablePagination(rows_per_page=50)
    @out clusterplot = PlotData[]

    @onchange isready, trees, algorithm, num_of_clusters begin
        # trees_matrix = split_weight(trees, num_of_taxa)
        datatable = DataTable(trees)
        trees_matrix = standardize_tree(Matrix(trees))
        trees_PCA = convertPCA(trees)
        result = kmeans_label(trees_matrix, num_of_clusters)
        trees_PCA[!, :label] = result
        clusterplot = plotdata(trees_PCA, :x1, :x2; groupfeature=:label)
    end
end

@page("/", "ui.jl")
Server.isrunning() || Server.up()
