# The INRS Audiovisual Quality Dataset

the details are given in publication [1]

File List:

MOS Folder: This Folder contains MOS Scores calculated. refer to the Readme file in this Folder for details.

OutputVideoFiles Folder: This Folder contains saved output video files, RTCP stats collected during streaming for each file, consolidated statistics and video file header parameters, and randomized file list used in https://github.com/edipdemirbilek/SubjectiveAssesmentVideoPlayer.

SourceVideoFiles Folder: It includes source video files, and audio and video CAPS used in GStreaming.

SubjectDetails Folder: It contains ACR scores collected from all observers. These are non processed raw scores. No consolidation or rejection criteria is applied.

SubjectMerged Folder: Consolidated ACR scores with summary info. The scores here are after rejection criteria is applied. Refer to [1] for details.

CalculateCorrelation.py: Calculates the correlation of scrores of a given Subject with the overall MOS of all Subjects.

GenerateGraphs.py: Generates variosu graphs used in [1]

MergeSubjectDetails.py: Consolidates the ACR scores for a given Subject and also applies the rejection criteria specified in [1]

MergeSubjects.py: Consolidate all Subject scores and compines with detailed parameters and generates varios MOS files. Comments in the file itself.

PrepareBitstreamStats.py: From GStreamer RTCP stats file, it extracts only selected fields and stores in csv file.

SubjectsSummary.csv: includes, total number of accepted scores, average time to rate and correlation to the rest for each subject.

[1] Demirbilek, Edip, and Jean-Charles Grégoire. “The INRS Audiovisual Quality Dataset." 2016 ACM Multimedia Conference (accepted).
