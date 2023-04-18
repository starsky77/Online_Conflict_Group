# Online_Conflict_Group
 
Run the following code to create the environment
```bash
conda env create -f environment.yaml
```

`Vis` contain the visualization result for each converstion and the content in each conversation.

Run `python3 DTW.py` to get the visualization result of the hierarchy clustering based on Dynamic Time Warping (DTW). The result is shown in `linkage_matrix.png`.

Run `python3 vis_group.py` to get each cluster's visualization result in `group_x_plots.png`

`vis_color.py` is used to get the visualization result of all the conversations, each user would have different color in the visualization result.

`vis.py` is used to create all the plots in `Vis`.
