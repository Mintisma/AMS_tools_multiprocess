It is a tool to facilitate the targeting of AMS ads.

How to Run it? (if you already have python installed and deployed) Just open your terminal and cd to the file where you store the folder of AMS_tools, then run "python ams_interact.py". Open the URL "http://127.0.0.1:8080/" as the terminal prompts.

The input is in a frame in the left, and you have two search modes with this tool.

The first one is search by category. If you want to find best selling speakers in www.amazon.com, you can try this url "https://www.amazon.com/gp/bestsellers/wireless/9977446011/" in which "9977446011" is the identifier. Thus you can just choose US as the country to browse and put "9977446011" in the "top 100_index".

The second one is search by keywords. Use it as what you usually do in your browser.

The outputs have three part, first one is a histgram in which price composes the x-axis, and y-axis is the number of items. The second part is a table containing details of skus you searched. The third parts is asins of the searching results for which you can just copy and paste into the browser for reference.
