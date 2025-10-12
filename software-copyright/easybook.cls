%%
%% This is file `easybook.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% easybook.dtx  (with options: `class')
%% Copyright (C) 2021-2024 by Qu Yi <toquyi@163.com>
%% 
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either
%% version 1.3c of this license or (at your option) any later
%% version. The latest version of this license is in:
%% 
%%   http://www.latex-project.org/lppl.txt
%% 
%% and version 1.3 or later is part of all distributions of
%% LaTeX version 2005/12/01 or later.
%% 
%% This work has the LPPL maintenance status `maintained'.
\NeedsTeXFormat{LaTeX2e}[2021/11/15]
\ProvidesExplClass{easybook}{2024/09/16}{2024dq}
  {Easily typesetting Chinese theses or books}

\bool_new:N \l__eb_compile_draft_bool
\bool_new:N \l__eb_title_newline_bool
\bool_set_true:N \l__eb_class_mode_book_bool
\clist_new:N \g__eb_doc_options_clist
\cs_new_protected:Npn \eb_put_ctexbook:n #1
  { \PassOptionsToClass{#1}{ctexbook} }
\cs_generate_variant:Nn \eb_put_ctexbook:n { V }

\keys_define:nn { easybook }
  {
    newline .code:n         = \bool_set_true:N \l__eb_title_newline_bool,
    scheme .code:n          = \eb_put_ctexbook:n { scheme = {#1} },
    enmode .meta:n          = { newline,scheme = plain },
    font .choices:nn        =
      { noto,times,times*,ebgaramond,libertine,palatino,auto }
      { \tl_set:Nn \l__eb_font_value_tl {#1} },
    font .value_required:n  = true,
    font .initial:n         = auto,
    cjkfont .code:n         = \eb_put_ctexbook:n { fontset = #1 },
    mathfont .tl_set:N      = \l__eb_mathfont_value_tl,
    mathfont .initial:n     = times,
    configs .clist_gset:N   = \g__eb_configs_file_clist, % For loading external settings.tex if still used
    paper .code:n           = { },
    class.code:n            = { },
    floatpage.code:n        = { },
    theorem .code:n         = { },
    unknown .code:n = \clist_gput_right:NV \g__eb_doc_options_clist \CurrentOption
  }

\cs_if_exist:NTF \ProcessKeyOptions
  { \ProcessKeyOptions[easybook] }
  {
    \RequirePackage{l3keys2e}
    \ProcessKeysOptions{easybook}
  }
\PassOptionsToPackage{no-math,quiet,CJKmath}{xeCJK}
\eb_put_ctexbook:V \g__eb_doc_options_clist
\LoadClass[UTF8, heading=true]{ctexbook}

\RequirePackage{easybase}

% Packages from settings.tex
\RequirePackage{tocloft} % For direct TOC control
\RequirePackage{fancyhdr}
\RequirePackage{subcaption}
\RequirePackage{booktabs}
\RequirePackage{makecell}
% \RequirePackage{array}
\RequirePackage{listings}
\RequirePackage{xcolor} % listings might load it, but explicit is fine
\RequirePackage{caption}
\RequirePackage{enumitem}
\RequirePackage{zhlipsum,bicaption,tcolorbox} % For document info commands

% \ctexset for main text formatting, geo, bib (merged from settings.tex)
% This will be applied after the class's initial \ctex_set:n, effectively merging/overriding.
% Alternatively, modify the class's own \ctex_set:n block directly.
% For clarity, we'll use a new \ctexset here.
\ctexset{ 
    section={ % Merged from settings.tex and class defaults
      hang = true, % from class
      format = \color{ctex@frame}\rmfamily\Large, % from class
      format+ = \raggedright\songti, % from settings.tex
      aftername = \hspace{0.5em}, % from class
      name = {,、}, % from settings.tex
      number = \chinese{section}, % from settings.tex
      beforeskip = 3.0ex plus 0.2ex minus .2ex, % from settings.tex (overrides class's 2ex...)
      afterskip = 1.0ex plus 0.2ex minus .2ex,  % from settings.tex (overrides class's 2ex...)
     },
    subsection={ % Merged
        hang = true,
        format = \color{ctex@frame}\rmfamily\large,
        format+ = \raggedright\songti,
        aftername = \hspace{0.2em},
        number = \arabic{section}.\arabic{subsection},
        beforeskip = 1.5ex plus .2ex minus .1ex, % from class (settings.tex didn't specify)
        afterskip = 1.5ex plus .2ex minus .1ex  % from class (settings.tex didn't specify)
    },
    subsubsection={ % Merged
        hang = true,
        format = \color{ctex@frame}\rmfamily, % from class
        format+ = \raggedright\songti\large, % from settings.tex
        aftername = \hspace{0.2em},
        number = \arabic{section}.\arabic{subsection}.\arabic{subsubsection},
        beforeskip = 1.0ex plus .2ex minus .1ex,  % from class (settings.tex didn't specify)
        afterskip = 1.0ex plus .2ex minus .1ex  % from class (settings.tex didn't specify)
    },
    paragraph = { % From settings.tex
        format+ = \noindent\raggedright\bfseries,
        name = {},
        numbering = false,
        beforeskip = 1.0ex plus 0.2ex minus 0.2ex,
        afterskip = 0.5ex plus 0.1ex minus 0.1ex,
        runin = false
    },
    geo = { % From settings.tex
        vmargin = {2.54cm,2.54cm},
        hmargin = 3.17cm,
        headheight = 2.04cm,
        headsep = 0.5cm,
        ignorefoot
    },
    % TOC formatting (indent, numwidth) will be handled by tocloft commands below.
    % The 'toc' key in the class's original \ctex_set:n is removed/commented out.
    % We still need to ensure tocdepth is set correctly.
    tocdepth = 3, % From settings.tex, ensuring it's set.
    bib = { % From settings.tex
        backend = bibtex,
        bib-style = numerical
    }
}

% 调整目录标题格式 (from settings.tex)
\renewcommand{\contentsname}{\songti 目\hspace{1em}录}

% 页眉页脚设置 (from settings.tex)
\definecolor{grey}{RGB}{136,136,136}
% fancyhdr is already required above
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\color{grey} 第\thepage 页}
\fancyhead[L]{\color{grey} \Version}
\fancyhead[C]{\color{grey} \Header}

% 默认图片路径 (from settings.tex)
\graphicspath{{images/}}

% \newcolumntype (from settings.tex)
\newcolumntype{Y}{>{\centering\arraybackslash}m{3cm}}
\newcolumntype{Z}{>{\centering\arraybackslash}X}

% 图表题注字体 (from settings.tex)
% caption package is already required above
% 设置图注字体
% 图表题注字体 (from settings.tex)
% caption package is already required above
\captionsetup[table]{font={rm}}
\captionsetup[figure]{font={rm}}
\captionsetup[lstlisting]{font={sf}}

% enumitem settings (from settings.tex)
% enumitem package is already required above
\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=$\circ$}
\setlist[itemize,3]{label=$\diamond$}
\setlist[itemize]{
    labelindent=2em,
    topsep=6pt,
    itemsep=\itemsep,
    parsep=\parsep
}

% listings styles and language definitions (from settings.tex)
% listings and xcolor packages are already required above
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{basecode}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    stringstyle=\color{codepurple},
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2,
    frame=single,
}
\lstdefinestyle{mystyle}{
    style=basecode,
    basicstyle=\ttfamily\normalsize,
    numbers=none,
    backgroundcolor={},
    frame=none
}
\lstdefinestyle{blockstyle}{
    style=basecode,
    basicstyle=\ttfamily\small,
    numbers=none,
    xleftmargin=1em,
    framexleftmargin=0.5em,
}
\lstdefinestyle{codestyle}{
    style=basecode,
    basicstyle=\ttfamily\scriptsize,
    numbers=none,
    numbersep=10pt,
    numberstyle=\tiny\color{codegray},
    xleftmargin=1em,
    framexleftmargin=0em,
}

\definecolor{jsonnum}{RGB}{94,129,81}
\definecolor{jsonbrace}{RGB}{63,81,181}

\lstdefinelanguage{json}{
    style=basecode,
    % basicstyle=\ttfamily\small,
    keywords={},
    keywordstyle=\color{magenta},
    commentstyle=\color{codegreen},
    stringstyle=\color{codepurple},
    morestring=[b]",
    morecomment=[l]//,
    morecomment=[s]{/*}{*/},
    literate=
    *{0}{{{\color{jsonnum}0}}}{1} {1}{{{\color{jsonnum}1}}}{1}
    {2}{{{\color{jsonnum}2}}}{1} {3}{{{\color{jsonnum}3}}}{1}
    {4}{{{\color{jsonnum}4}}}{1} {5}{{{\color{jsonnum}5}}}{1}
    {6}{{{\color{jsonnum}6}}}{1} {7}{{{\color{jsonnum}7}}}{1}
    {8}{{{\color{jsonnum}8}}}{1} {9}{{{\color{jsonnum}9}}}{1}
    {:}{{{\color{codegreen}{:}}}}{1}
    {,}{{{\color{codegreen}{,}}}}{1}
    {\{}{{{\color{jsonbrace}{\{}}}}{1}
    {\}}{{{\color{jsonbrace}{\}}}}}{1}
    {[}{{{\color{jsonbrace}{[}}}}{1}
    {]}{{{\color{jsonbrace}{]}}}}{1}
}
\lstdefinelanguage{Javascript}{
    morekeywords=[1]{break, continue, delete, else, for, function, if, in,
        new, return, this, typeof, var, void, while, with},
    morekeywords=[2]{false, null, true, boolean, number, undefined,
        Array, Boolean, Date, Math, Number, String, Object},
    morekeywords=[3]{eval, parseInt, parseFloat, escape, unescape},
    sensitive,
    morecomment=[s]{/*}{*/},
    morecomment=[l]//,
    morecomment=[s]{/**}{*/},
    morestring=[b]',
    morestring=[b]"
}[keywords, comments, strings]

% YAML Language Definition
\lstdefinelanguage{yaml}{
    style=basecode,
    keywords={true,false,null,True,False,NULL,yes,no,on,off},
    keywordstyle=\color{magenta},
    commentstyle=\color{codegreen},
    stringstyle=\color{codepurple},
    morecomment=[l]{\#},
    morestring=[b]",
    morestring=[b]',
    sensitive=true,
    literate=
    *{:}{{{\color{codegreen}{:}}}}{1}
    {-}{{{\color{jsonnum}{-}}}}{1}
    {|}{{{\color{jsonbrace}{|}}}}{1}
}

% Python Language Enhancement  
\lstdefinelanguage{python}{
    morekeywords=[1]{import,from,as,def,class,if,else,elif,for,while,try,except,finally,with,return,yield,pass,break,continue,and,or,not,in,is,lambda},
    morekeywords=[2]{str,int,float,bool,list,dict,tuple,set,None,True,False},
    sensitive=true,
    morecomment=[l]{\#},
    morestring=[b]',
    morestring=[b]"
}[keywords, comments, strings]

% Bash Language Definition
\lstdefinelanguage{bash}{
    morekeywords=[1]{cd,ls,mkdir,cp,mv,rm,chmod,grep,find,which,export,source,python,pip,conda,git,make,cmake},
    morekeywords=[2]{--help,--config,--group,--analysis-types,--output},
    sensitive=true,
    morecomment=[l]{\#},
    morestring=[b]',
    morestring=[b]"
}[keywords, comments, strings]

% --- Settings integrated from settings.tex END ---

\ctex_at_end_preamble:n
  {
    \use:c { eb@font@load@\l__eb_font_value_tl } % Class's font loading
    % If settings.tex was loaded via 'configs' option, it would happen here.
    % Since we are integrating, we assume settings.tex is not loaded via 'configs'.
    % \clist_if_empty:NF \g__eb_configs_file_clist
    %   { \clist_map_function:NN \g__eb_configs_file_clist \file_input:n }
  }

\sys_if_engine_xetex:TF
  {
    \cs_new_eq:NN \eb_set_family:nnn \xeCJK_set_family:nnn
    \cs_new_eq:NN \eb_switch_family:n \xeCJK_switch_family:n
  }
  {
    \cs_new_eq:NN \eb_set_family:nnn \ctex_ltj_set_family:nnn
    \cs_new_eq:NN \eb_switch_family:n \ctex_ltj_switch_family:n
  }
\cs_generate_variant:Nn \eb_set_family:nnn { x }
\cs_new_protected:Npn \eb_setmainfont:nn #1#2
  { \__fontspec_main_setmainfont:nn {#2} {#1} }
\cs_new_protected:Npn \eb_setsansfont:nn #1#2
  { \__fontspec_main_setsansfont:nn {#2} {#1} }
\cs_new_protected:Npn \eb_setmonofont:nn #1#2
  { \__fontspec_main_setmonofont:nn {#2} {#1} }
\cs_new_protected:Npn \eb_setCJKmainfont:nn #1#2
  { \eb_set_family:xnn { \CJKrmdefault } {#2} {#1} }
\cs_new_protected:Npn \eb_setCJKsansfont:nn #1#2
  { \eb_set_family:xnn { \CJKsfdefault } {#2} {#1} }
\cs_new_protected:Npn \eb_setCJKmonofont:nn #1#2
  { \eb_set_family:xnn { \CJKttdefault } {#2} {#1} }
\clist_map_inline:nn
  { main,sans,mono,CJKmain,CJKsans,CJKmono }
  {
    \exp_args:Nc \RenewDocumentCommand { set#1font }{O{}mO{}}
      {\use:c { eb_set#1font:nn } {##2} { ##1,##3 }}
  }
\RenewDocumentCommand{\newCJKfontfamily}{omO{}mO{}}
  {
    \tl_set:Nx \l_tmpa_tl { \tl_if_novalue:nTF {#1} { \cs_to_str:N #2 } {#1} }
    \cs_new_protected:Npx #2 { \eb_switch_family:n { \l_tmpa_tl } }
    \eb_set_family:xnn { \l_tmpa_tl } { #3,#5 } {#4}
  }

\cs_new_protected:Npn \eb@font@load@noto
  {
    \eb_setmainfont:nn { NotoSerif }
      {
        Extension   = .ttf,
        UprightFont = *-Regular,
        BoldFont    = *-Bold,
        ItalicFont  = *-Italic
      }
    \eb_setsansfont:nn { NotoSans }
      {
        Extension   = .ttf,
        UprightFont = *-Regular,
        BoldFont    = *-Bold,
        ItalicFont  = *-Italic
      }
    \eb_setmonofont:nn { NotoSansMono }
      {
        Extension   = .ttf,
        UprightFont = *-Regular,
        BoldFont    = *-Bold
      }
  }
\cs_new_protected:Npn \eb@font@load@times
  {
    \eb_setmainfont:nn { XITS }
      {
        Extension       = .otf,
        UprightFont     = *-regular,
        BoldFont        = *-bold,
        ItalicFont      = *-italic,
        BoldItalicFont  = *-bolditalic
      }
    \eb_setsansfont:nn { texgyreheros }
      {
        Extension       = .otf,
        UprightFont     = *-regular,
        BoldFont        = *-bold,
        ItalicFont      = *-italic,
        BoldItalicFont  = *-bolditalic
      }
    \eb_setmonofont:nn { texgyrecursor }
      {
        Extension       = .otf,
        UprightFont     = *-regular,
        BoldFont        = *-bold,
        ItalicFont      = *-italic,
        BoldItalicFont  = *-bolditalic,
        Ligatures       = CommonOff
      }
  }
\cs_new_protected:cpn { eb@font@load@times* }
  {
    \eb_setmainfont:nn { Times~New~Roman } { }
    \eb_setsansfont:nn { Arial } { }
    \eb_setmonofont:nn { Courier~New } { }
  }
\cs_new_protected:Npn \eb@font@load@libertinus@sans
  {
    \eb_setsansfont:nn { LibertinusSans }
      {
        Extension   = .otf,
        UprightFont = *-Regular,
        BoldFont    = *-Bold,
        ItalicFont  = *-Italic
      }
  }
\cs_new_protected:Npn \eb@font@load@lmmonolt@mono
  {
    \eb_setmonofont:nn { lmmonolt10 }
      {
        Extension       = .otf,
        UprightFont     = *-regular,
        BoldFont        = *-bold,
        ItalicFont      = *-oblique,
        BoldItalicFont  = *-boldoblique
      }
  }
\cs_new_protected:Npn \eb@font@load@ebgaramond
  {
    \eb_setmainfont:nn { EBGaramond }
      {
        Extension       = .otf,
        UprightFont     = *-Regular,
        BoldFont        = *-Bold,
        ItalicFont      = *-Italic,
        BoldItalicFont  = *-BoldItalic
      }
    \eb@font@load@libertinus@sans
    \eb@font@load@lmmonolt@mono
  }
\cs_new_protected:Npn \eb@font@load@libertine
  {
    \eb_setmainfont:nn { LibertinusSerif }
      {
        Extension       = .otf,
        UprightFont     = *-Regular,
        BoldFont        = *-Bold,
        ItalicFont      = *-Italic,
        BoldItalicFont  = *-BoldItalic
      }
    \eb@font@load@libertinus@sans
    \eb@font@load@lmmonolt@mono
  }
\cs_new_protected:Npn \eb@font@load@palatino
  {
    \eb_setmainfont:nn { texgyrepagella }
      {
        Extension       = .otf,
        UprightFont     = *-regular,
        BoldFont        = *-bold,
        ItalicFont      = *-italic,
        BoldItalicFont  = *-bolditalic
      }
    \eb@font@load@libertinus@sans
    \eb@font@load@lmmonolt@mono
  }
\cs_new_protected:Npn \eb_put_newtxmath:n #1
  { \PassOptionsToPackage{#1}{newtxmath} }
\cs_generate_variant:Nn \eb_put_newtxmath:n { V }
\str_case:VnF \l__eb_mathfont_value_tl
  {
    { times } { \RequirePackage{newtxmath,bm} }
    { none } { }
  }
  {
    \eb_put_newtxmath:V \l__eb_mathfont_value_tl
    \RequirePackage{newtxmath,bm}
  }

% Original \ctex_set:n from easybook.cls for part, chapter, and main text sectioning formats
% The 'toc' key for indent/numwidth has been removed from here,
% as we are using tocloft commands for that.
% However, 'tocdepth' and 'secnumdepth' are still relevant here.
\ctex_set:n
  {
    secnumdepth     = 3, % Number sections down to subsubsection in text
    tocdepth        = 3, % Default TOC depth (can be overridden by user's \ctexset or \setcounter)
    part            =
      {
        pagestyle   = empty,
        format      = \color{ctex@frame}\sffamily\Huge,
        nameformat  = { },
        titleformat = { },
        aftername   =
          {
            \bool_if:NTF \l__eb_title_newline_bool
              { \par\nobreak }
              { \hspace{1em} }
          }
      },
    chapter         =
      {
        pagestyle   = empty,
        format      =
          {
            \color{ctex@frame}\sffamily\LARGE
            \bool_if:NF \l__eb_title_newline_bool { \centering }
          },
        nameformat  = { },
        titleformat = { },
        aftername   =
          {
            \bool_if:NTF \l__eb_title_newline_bool
              { \par\nobreak\vskip 1.5pc }
              { \hspace{1em} }
          },
        beforeskip  = 0pt,
        afterskip   = 25pt
      }
    % section, subsection, subsubsection text formatting is now handled by the \ctexset block
    % that was integrated from settings.tex earlier in this file.
    % paragraph text formatting is also handled by that integrated block.
    % geo and bib are also handled by that integrated block.
  }
\bool_if:NF \l__eb_title_newline_bool
  {
    \ctex_set:n
      {
        part/hang     = true,
        chapter/hang  = true
      }
  }
\endinput
%% 
%% End of file `easybook.cls'.
