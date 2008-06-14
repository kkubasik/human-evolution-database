from django.conf.urls.defaults import *

urlpatterns = patterns(
    'humanevo.views',
    (r'^$', 'index'),
    (r'^all$', 'all'),
#===============================================================================
#    (r'^mine$', 'mine'),
    (r'^new$', 'new'),
#    (r'^upload$', 'upload'),
    (r'^(.*)$', 'show'),
    (r'^(.*)/show$', 'show'),
#    (r'^(\d+)/add$', 'add'),
    (r'^(.*)/edit$', 'edit'),
#    (r'^(\d+)/delete$', 'delete'),
#    (r'^(\d+)/publish$', 'publish'),
#    (r'^(\d+)/download/(\d+)', 'download'),
#    (r'^(\d+)/patch/(\d+)/(\d+)$', 'patch'),
#    (r'^(\d+)/diff/(\d+)/(\d+)$', 'diff'),
#    (r'^(\d+)/diff2/(\d+):(\d+)/(\d+)$', 'diff2'),
#    (r'^(\d+)/diff_skipped_lines/(\d+)/(\d+)/(\d+)/(\d+)/([tb])$',
#     'diff_skipped_lines'),
#    (r'^(\d+)/diff2_skipped_lines/(\d+):(\d+)/(\d+)/(\d+)/(\d+)/([tb])$',
#     'diff2_skipped_lines'),
#    (r'^inline_draft$', 'inline_draft'),
#    (r'^repos$', 'repos'),
#    (r'^repo_new$', 'repo_new'),
#    (r'^repo_init$', 'repo_init'),
#    (r'^branch_new/(\d+)$', 'branch_new'),
#    (r'^branch_edit/(\d+)$', 'branch_edit'),
#    (r'^branch_delete/(\d+)$', 'branch_delete'),
#    (r'^settings$', 'settings'),
#===============================================================================
    )
