
test_oeb:
	test -d lwn_weekly_oeb && rm -rf lwn_weekly_oeb || :
	ebook-convert lwn_weekly.recipe lwn_weekly_oeb --test -vvvvv -d debug

test_mobi:
	ebook-convert lwn_weekly.recipe .mobi --test -vvvvv -d debug

test_epub:
	ebook-convert lwn_weekly.recipe .epub --test -vvvvv -d debug

mobi:
	ebook-convert lwn_weekly.recipe lwn_weekly.mobi

epub:
	ebook-convert lwn_weekly.recipe lwn_weekly.epub
