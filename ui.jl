[
    # insert contents of string var. using double mustache {{}} syntax
    heading("{{title}}")row([
        # selectors
        cell(
            class="st-module",
            [
                h6("Algorithm")
                Stipple.select(:algorithm; options=:algorithms);
                textfield(
                    "Number of Clusters",
                    :num_of_clusters,
                    bottomslots="",
                    dense="",
                )
            ]
        )cell(
            class="st-module",
            [
                h6("Parameters")]
        )
        # data
        # cell(
        #     class="st-module",
        #     [
        #         h6("Upload trees in .csv")
        #         uploader(
        #             multiple=true,
        #             accept=:upl_acceptext,
        #             maxfilesize=:upl_maxsize,
        #             maxfiles=10,
        #             autoupload=true,
        #             hideuploadbtn=true,
        #             nothumbnails=true,
        #             style="max-width: 95%; width: 95%; margin: 0 auto;",
        #             @on("rejected", :rejected),
        #             @on("uploaded", :uploaded),
        #             @on("finish", :finished),
        #             @on("failed", :failed),
        #             @on("uploading", :uploading),
        #             @on("start", :started),
        #             @on("added", :added),
        #             @on("removed", :removed)
        #         )
        #     ]
        # )
    ])
    # plots
    row([
        cell(
            class="st-module",
            [
                h5("Clustering Result")
                plot(:clusterplot)
            ]
        )
    ])
    # table
    row([
        cell(
            class="st-module",
            [
                h5("Trees")
                GenieFramework.table(:datatable; dense=true, flat=true, style="height: 350px;", pagination=:datatablepagination)
            ]
        )
    ])
] |> string
