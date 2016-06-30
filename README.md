# The INRS Audiovisual Quality Dataset

the details are given in publication [1]

File List:

MOS Folder: This Folder contains MOS Scores calculated. refer to the Readme file in this Folder for details.

OutputVideoFiles Folder: This Folder contains saved output video files, RTCP stats collected during streaming for each file, consolidated statistics and video file header parameters, and randomized file list used in https://github.com/edipdemirbilek/SubjectiveAssesmentVideoPlayer.

SourceVideoFiles Folder: It includes source video files, and audio and video CAPS used in GStreaming.

SubjectDetails Folder: It contains ACR scores collected from all observers. These are non processed raw scores. No consolidation or rejection criteria is applied.

SubjectMerged Folder: Consolidated ACR scores with summary info. The scores here are after rejection criteria is applied. Refer to [1] for details.

CalculateCorrelation.py:

GenerateGraphs.py:

MergeSubjectDetails.py:

MergeSubjects.py:

PrepareBitstreamStats.py:

SubjectsSummary.csv:

[1] Demirbilek, Edip, and Jean-Charles Grégoire. “The INRS Audiovisual Quality Dataset." 2016 ACM Multimedia Conference (accepted).
