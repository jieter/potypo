from potypo.filters import HTMLFilter, PythonFormatFilter, make_EdgecaseFilter


def assert_filter(filter, expect_skip, expect_noskip):
    SKIP_MSG_FMT = "String '{s}' should be skipped by {filter_name}, but is not."
    NOSKIP_MSG_FMT = "String '{s}' should not be skipped by {filter_name}"
    filter_name = filter.__class__

    for s in expect_skip:
        assert filter._skip(s), SKIP_MSG_FMT.format(**locals())

    for s in expect_noskip:
        assert not filter._skip(s), NOSKIP_MSG_FMT.format(**locals())


def test_EdgecaseFilter():
    edgecase_words = 'add-ons MT940 pre-selected myblog.org myproject.org-Blog myproject.org-Server 4th'.split()
    expect_skip = edgecase_words
    expect_noskip = ('addons', 'preselected', 'myproject.org')

    filter = make_EdgecaseFilter(edgecase_words)(object())
    assert_filter(filter, expect_skip, expect_noskip)


def test_HTMLFilter():

    expect_skip = ('&lt;html&gt;', '&lt;p&gt;', )
    expect_noskip = ('', 'django', 'V&D')

    # pass a fake tokenizer
    assert_filter(HTMLFilter(object()), expect_skip, expect_noskip)


def test_PythonFormatFilter():

    expect_skip = ('%(django)', '{potypo}', )
    expect_noskip = ('', 'django', '10%')

    # pass a fake tokenizer
    assert_filter(PythonFormatFilter(object()), expect_skip, expect_noskip)
