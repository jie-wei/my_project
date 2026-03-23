$pdf_mode = 5;
$do_cd    = 1;
$aux_dir  = '.build';
$success_cmd = 'rm -rf .build && rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log main.out main.synctex.gz';

use Cwd qw(abs_path);
use File::Basename;
my $paper_dir = dirname(abs_path(__FILE__));
my $templates = abs_path("$paper_dir/../docs/templates/latex");

ensure_path('TEXINPUTS', "$paper_dir//:$templates//:.");
ensure_path('BIBINPUTS', "$paper_dir//:$templates//:.");
ensure_path('BSTINPUTS', "$paper_dir//:$templates//:.");
