### on the devserver
## run the following commands after you have the GAIA ids
## Find the GAIA ids here: https://docs.google.com/spreadsheets/d/1-sEQCyvbvbHQFSqbl5XCyza3iNnQi1llZGFdftKAuoM/edit#gid=2048077995
## they will be uploaded to https://www.internalfb.com/manifold/explorer/spaceport_data/tree/rawalProject


# cd /data/users/rawalk/fbsource/fbcode/surreal/aria_research_tools
# buck build -c python.package_style=inplace --show-output //surreal/aria_research_tools:run_merge_recordings_simple
# $HOME/fbsource/fbcode/buck-out/gen/surreal/aria_research_tools/run_merge_recordings_simple.par --excluded_stream_ids  285 --parent_ids [list of GAIA_IDS]

### aria01 and aria02
# cd /data/users/rawalk/fbsource/fbcode/surreal/aria_research_tools
# buck build -c python.package_style=inplace --show-output //surreal/aria_research_tools:run_merge_recordings_simple
# $HOME/fbsource/fbcode/buck-out/gen/surreal/aria_research_tools/run_merge_recordings_simple.par --excluded_stream_ids  285 --parent_ids 1734630476901520 1954516401605238 865269541113723 5273127309435193 466078801723481 804928087337433


# ### aria03 and aria04
# # cd /data/users/rawalk/fbsource/fbcode/surreal/aria_research_tools
# buck build -c python.package_style=inplace --show-output //surreal/aria_research_tools:run_merge_recordings_simple
# $HOME/fbsource/fbcode/buck-out/gen/surreal/aria_research_tools/run_merge_recordings_simple.par --excluded_stream_ids  285 --parent_ids 1120979198454847 1249537799211084 1656706208047102 757897562191728 790039588794009 426067416216805


# # ### aria05 and aria06
# # cd /data/users/rawalk/fbsource/fbcode/surreal/aria_research_tools
# buck build -c python.package_style=inplace --show-output //surreal/aria_research_tools:run_merge_recordings_simple
# $HOME/fbsource/fbcode/buck-out/gen/surreal/aria_research_tools/run_merge_recordings_simple.par --excluded_stream_ids  285 --parent_ids 1011430629549683 733815391031759 764245114818138 469364431330744 753848652701712 3172966819683702



# ### aria01
# cd /data/users/rawalk/fbsource/fbcode/surreal/aria_research_tools
buck build -c python.package_style=inplace --show-output //surreal/aria_research_tools:run_merge_recordings_simple
$HOME/fbsource/fbcode/buck-out/gen/surreal/aria_research_tools/run_merge_recordings_simple.par --excluded_stream_ids  285 --parent_ids 618567999392322