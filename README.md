# From Videos to Classification Dataset
Tool that extracts the frames from videos generating a classification dataset.

#### How to use this tool

Simply run the file `video_extractor.py` after having correctly set its parameters and folder structure.

#### Video Preparation

The videos should be in `mp4` format, and they should be named after the class they contain (`firstclass.mp4`, `firstclass1.mp4`, `secondclass.mp4`...). In this way there can be many videos belonging to the same class.

#### Parameters and Options

1. **size_validation**: percentage of images randomly selected to be part of the validation set (`/data/validation_set`)
2. **equilibrate_classes**: if *True*, some frames are removed from the training set in order to obtain a dataset with the same number of images per class (balanced dataset).

This tool automatically generates the folders it needs and reorder randomly the frames renaming them according to their class.

#### Dependencies

The following packages are needed to run this tool:

- OpenCV
- os
- random
- numpy
- [fuckit](https://github.com/ajalt/fuckitpy) (used to ignore errors when generating already existing folders)