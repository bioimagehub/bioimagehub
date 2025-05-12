# Bioimage-processing-hub
## About Our Facility
The **Bioimage Processing Hub (BIPHUB)** is a collaborative effort intended to provide a resource that supports microscopists at the imaging nodes across Oslo. My role will be to help users develop image analysis pipelines.
Whether you're working with datasets from the Montebello Node, Blindern Node, IMB node, or Gaustad node, I can assist you with your image analysis pipelines and encourage you to reach out.

### Contact info
You can contact me via email at biphub-contact@medisin.uio.no to set up a meeting. Currently  I am dedicating a 50 % position to image analysis and if a lot of requests are made some priorities might be made.  I can work in several programming ImageJ, Python, Go, MATLAB and other programming languages, and have access to several powerful computers and software, that are needed for various challenges.
When you send an email it will automatically create a request in the request tracker, so please give an informative subject header to your email. And all requests must be submitted this way.
Please ensure that you include this information in your request:
1.	Your name and the name of your PI (Group Leader):
2.	The name of your imaging node (Montebello Node, Blindern Node, IMB node, or Gaustad node):
3.	A link to some example files (not the entire dataset if large):
4.	A detailed description of your problem and what you need assistance with:
5.	Should the generated code be available for the public?: (Yes/ No/ Only after yyyy.mm.dd/publication/etc)
6. Would you like to join a mailing list where I send out occational updates about code that is avalable for everyone.

### Bioimage-processing-hub email list
If you wish to recieve occational emails about what I am currently working on/releasing you can email me at bioimagehub@gmail.com and I will add you to my email list. Please include you Name, Group leader name, and which imaging node you belong to (Montebello Node, Blindern Node, IMB node, or Gaustad node). 

## NEW / in progress !!!
### Workflow manager. [run_pipeline.exe](https://github.com/bioimagehub/run_pipeline)
Check out my new program that can execute all your other scripts sequentially while keeping a record of what processing steps have been done.
The aim of this is to move towards automated image analysis and the idea is that you have a folder of images going into the pipeline and an results table / plots coming out in the other end. 
If this is interesting to you please contact me or try it out!

You can write your own programs, use programs developed by others, or use code from the [standard_code](https://github.com/bioimagehub/run_pipeline/tree/main/standard_code).
Currently I have tested this on:
* Cellpose
* All the programs in [standard_code](https://github.com/bioimagehub/run_pipeline/tree/main/standard_code)
But in essence if you can run your program from a windows terminal it should work.

In brief:
You need to have python (miniconda or anaconda installed)
You need to have the python environments that you need to run your code [example python environments](https://github.com/bioimagehub/run_pipeline/tree/main/conda_envs)
You need to make a config file: or use one of these [example workflow files](https://github.com/bioimagehub/run_pipeline/tree/main/pipeline_configs)
The yaml file should look something like this:
```yaml
run:
- name: Collapse folder structure and save as .tif # A name that describes this part of the code
  environment: drift # name of the python environment you want to call
  commands: # This is a list of commands that you want to execute
  - python
  - ./standard_code/convert_to_tif.py " # You can add the full path to your 
  - --input_folder: ./input
  - --extension: .ims
  - --search_subfolders
  - --collapse_delimiter: __
  - --projection_method: sum
- name: run find nuclei with threshold # Once the first run comand has been executed this will run.
  environment: segment
  commands:
  - python
  - ./standard_code/segment_threshold.py
  - --input_folder: ./input_tif
  - --output_folder: ./output_nuc_mask
  - --channels: 3
  - --median_filter_size: 15
  - --method: li
  - --min_size: 10000
  - --max_size: 55000
  - --watershed_large_labels
  - --remove_xy_edges
```




- **Email:** [biphub-contact@medisin.uio.no](mailto:biphub-contact@medisin.uio.no)

Øyvind Ødegård Fougner
Bioimage Processing Hub (BIPHUB)

