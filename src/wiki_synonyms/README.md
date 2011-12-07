File Description
=====================

* wiki.original.txt
    - INPUT: None
    - Description: 
        * This file includes the information for all wikipages
        * Each line is the record for a page.
    - Format: &lt;page\_id&gt;&lt;tab&gt;&lt;title&gt;
    - Note: Title format is "AccessibleComputing". Not separated by space.
* wiki.redirect.txt
    - INPUT: None
    - Description
        * This file contains all information about _redirected_ pages
        * Each line is the record for a page.
    - Format: &lt;page\_id&gt;&lt;tab&gt;&lt;title&gt;
    - Note: The title is space delimited.
* wiki.id.from.to.txt
    - INPUT: wiki.redirect.txt wiki.original.txt
    - Description
        * Each line includes the info for the Redirect from 
    - Format: &lt;page\_id&gt;&lt;tab&gt;&lt;from\_title&gt;&lt;tab&gt;&lt;to\_title&gt;
    - Note: the from title format is still blah ..
* wiki.synonyms.txt
    - INPUT: wiki.id.from.to.txt
    - Description
    - Format: Each line is a group of synonyms, separated by "\t"

Strategy
=====================
Keep Original: wiki.id.from.to.txt



