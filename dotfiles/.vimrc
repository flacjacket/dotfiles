" .vimrc

" pathogen
call pathogen#infect()

" set UTF-8 encoding
set enc=utf-8
set fenc=utf-8
set termencoding=utf-8

" detect filetype
filetype plugin indent on
set autoindent
set smartindent

" enable syntax hightligting
syntax on

" disable vi compatibility
set nocompatible

" turn on line numbers
set number

" status and Info
set ruler
set title
set showcmd
set ls=2
set confirm
set report=0
set laststatus=2

" improved searching
set incsearch
set ignorecase
set smartcase
set hlsearch
set incsearch
set showmatch

" tabbing settings
set tabstop=4
set shiftwidth=4
set expandtab
au BufRead,BufNewFile *.tex set shiftwidth=2
au BufRead,BufNewFile *.tex set tabstop=2
au BufRead,BufNewFile *.sty set shiftwidth=2
au BufRead,BufNewFile *.sty set tabstop=2
au BufRead,BufNewFile *.tex set textwidth=80
"au BufEnter *.hs compiler ghc
set smarttab
set scrolloff=3

" better dealing with multiple buffers
set hidden

" better command-line completion
set wildmenu

" allow backspacing over autoindent, line breaks and start of insert action
set backspace=indent,eol,start

" show matching brackets
set showmatch

" allows folding by whitespace
set foldmethod=indent
set foldlevel=99

" reading/Writing
set noautowrite
set noautowriteall
set noautoread
set ffs=unix,dos,mac

" for when you forget to use sudo to open a file
cmap c!! w !sudo tee % >/dev/null

" highlite end-of-line whitespace
hi ExtraWhitespace ctermbg=Red
au InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
au InsertLeave * match ExtraWhitespace /\s\+$/

" --------
" Mappings
" --------

" Map <C-L> (redraw screen) to also turn off search highlighting until the next search
nno <C-L> :nohl<CR><C-L>

" Map :W to :w and :Q to :q
cm W w
cm Q q

" Dvorak re-bindings
no t k
no T gk
no n j
no N gj
no s l
no S L

no k n
no j N

" Bind moving windows
no <c-h> <c-w>h
no <c-t> <c-w>k
no <c-n> <c-w>j
no <c-s> <c-w>l

" Hardcore mode
no <Up> <nop>
no <Down> <nop>
no <Left> <nop>
no <Right> <nop>
