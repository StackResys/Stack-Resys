DATA_DIR=repo

# mysql wiki -uroot -p < dump_redirect_page.sql | python clean_redirect_page.py

$(DATA_DIR)/wiki.synonyms.txt: $(DATA_DIR)/wiki.id.from.to.txt
	python group_synonyms.py < $^ > $@

$(DATA_DIR)/wiki.id.from.to.txt: $(DATA_DIR)/wiki.original.txt \
						    		$(DATA_DIR)/wiki.redirect.txt
	python merge.py $^ > $(DATA_DIR)/wiki.id.from.to.txt
$(DATA_DIR)/wiki.redirect.txt: $(DATA_DIR)/wiki.redirect_pages.dump
	python clean_redirect_page.py < $^ > $@


clean:
	rm -rf $(DATA_DIR)/wiki.id.from.to.txt
