DATA_DIR=data
ORIGIN=origin

# mysql wiki -uroot -p < dump_redirect_page.sql | python clean_redirect_page.py


$(DATA_DIR)/wiki.synonyms.reduced.txt: $(DATA_DIR)/wiki.synonyms.normalized.txt
	python filter_non_english.py $^ > $@

$(DATA_DIR)/wiki.synonyms.normalized.txt: $(DATA_DIR)/wiki.synonyms.txt
	python normalize_synonym.py $^ > $@

$(DATA_DIR)/wiki.synonyms.txt: $(DATA_DIR)/wiki.id.from.to.txt
	python group_synonyms.py < $^ > $@

$(DATA_DIR)/wiki.id.from.to.txt: $(ORIGIN)/wiki.original.txt \
						    		$(DATA_DIR)/wiki.redirect.txt
	python merge.py $^ > $(DATA_DIR)/wiki.id.from.to.txt
$(DATA_DIR)/wiki.redirect.txt: $(ORIGIN)/wiki.redirect_pages.dump
	python clean_redirect_page.py < $^ > $@

clean:
	rm -rf $(DATA_DIR)/*
