$pdf_mode = 5;
$do_cd    = 1;
$aux_dir  = '.build';
$success_cmd = 'rm -rf .build && rm -f %R.aux %R.bbl %R.blg %R.fdb_latexmk %R.fls %R.log %R.out %R.synctex.gz %R.toc';

use Cwd qw(abs_path);
use File::Basename;
my $paper_dir = dirname(abs_path(__FILE__));
my $templates = abs_path("$paper_dir/../docs/templates/latex");

ensure_path('TEXINPUTS', "$paper_dir//:$templates//:.");
ensure_path('BIBINPUTS', "$paper_dir//:$templates//:.");
ensure_path('BSTINPUTS', "$paper_dir//:$templates//:.");
