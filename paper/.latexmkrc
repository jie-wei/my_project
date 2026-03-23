$pdf_mode = 5;
$do_cd    = 1;
$aux_dir  = '.build';
$success_cmd = 'rm -rf .build && rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log main.out main.synctex.gz';

ensure_path('TEXINPUTS', './/:');
ensure_path('TEXINPUTS', '../docs/templates/latex//:');
ensure_path('BIBINPUTS',  './/:');
ensure_path('BIBINPUTS',  '../docs/templates/latex//:');
ensure_path('BSTINPUTS',  './/:');
ensure_path('BSTINPUTS',  '../docs/templates/latex//:');
