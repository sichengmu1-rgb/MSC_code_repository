%# -*- coding: utf-8-unix -*-
%======================================================================
% qbook.cls for Qbook Template
%======================================================================
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{qbook}[2020/07/07 v2.05 Qbook Template]
\def\version{Version 2.05}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexbook}}
\ProcessOptions\relax
\PassOptionsToClass{scheme=chinese}{ctexbook}
\PassOptionsToClass{zihao=-4}{ctexbook}
\PassOptionsToPackage{no-math}{fontspec}
\LoadClass[a4paper,UTF8]{ctexbook}
%======================================================================
% 导入 qbook.cfg 文件
\AtEndOfClass{\input{qbook.cfg}} 
%======================================================================
% 导入 LaTeX 宏包
\RequirePackage{aliascnt} %用来复制计数器
\RequirePackage{tensor} % 用来严格区分张量的类型，预留出指标升降的空位
\RequirePackage{cancel} %用来在数学式子上画斜线
\RequirePackage{extarrows}
\RequirePackage{eso-pic}
\RequirePackage{url}
\RequirePackage{environ}
\RequirePackage{manfnt,pifont}
\RequirePackage{titlesec}
\RequirePackage{float}
\RequirePackage{wallpaper}
\RequirePackage[most]{tcolorbox}
\RequirePackage{xpatch}
\RequirePackage[centering,a4paper,body={16cm,22cm}]{geometry} 
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{amsmath,mathtools,amsthm,amsfonts,amssymb,bm}
\RequirePackage[defaultsups]{newtxtext}
\RequirePackage{newtxmath}
\RequirePackage{sourcecodepro}
\RequirePackage{upgreek}
\RequirePackage{wasysym}
\RequirePackage{anyfontsize}
\RequirePackage{metalogo,doc}
\RequirePackage{array}
\RequirePackage{threeparttable}
\RequirePackage{dcolumn}
\RequirePackage{multirow}
\RequirePackage{booktabs}
\RequirePackage{graphicx}
\RequirePackage[labelformat=empty]{caption}
\RequirePackage[list=off]{bicaption}
\RequirePackage{subcaption}
\RequirePackage[backend=biber,hyperref=auto,maxnames=4]{biblatex}
\RequirePackage{xcolor}
\RequirePackage{listings}
\RequirePackage[unicode, xetex, bookmarksnumbered,  plainpages=false, pdfstartview=FitH]{hyperref}
\RequirePackage{varioref}
\RequirePackage{bookmark}
\bookmarksetup{
	open,	
	numbered,
	color=purple
}
\RequirePackage{longtable}
\RequirePackage[perpage, bottom]{footmisc}
\RequirePackage[inline]{enumitem}
\RequirePackage{pdfpages}
\RequirePackage{calc}
\RequirePackage{algorithm, algorithmicx, algpseudocode}
\RequirePackage{siunitx}
\RequirePackage{tikz}

%======================================================================
% 导入tikz库
\usetikzlibrary{shapes.geometric, arrows}
\usetikzlibrary{shapes,decorations}
\usetikzlibrary{intersections,decorations.text}
%======================================================================
% 超链接设置及PDF文件信息
\hypersetup{
%	colorlinks,linkcolor=purple,linkbordercolor=purple, 彩色链接
	pdfauthor = {333},
	pdftitle = {QbookTemplate},
	pdfkeywords = {书籍模板}}
%======================================================================
% 添加水印命令\watermark{height}{angle1}{angle2}
\newcommand{\watermark}[3]{\newbox\@watermark@box %
						   \sbox\@watermark@box{\includegraphics[totalheight=#1\textwidth,angle=#2]{figure/watermark2.pdf}} % 水印图片
						   \def\@watermark@CMD{\ifodd\c@page\usebox\@watermark@box\else\rotatebox{#3}{\usebox\@watermark@box}\fi} %奇偶数页的风格
						   \AddToShipoutPictureBG{\AtTextCenter{\makebox(0,0)[c]{\@watermark@CMD}}} %
						   }
%======================================================================
% 自定义颜色
\definecolor{ocre}{RGB}{243,102,25} 
\definecolor{LightGoldenrod}{RGB}{238,221,130}
\definecolor{sthlmGreen}{RGB}{0,134,127}
\definecolor{Gold}{RGB}{255,215,0}
\definecolor{C1}{RGB}{32,88,153}
\definecolor{C2}{RGB}{218,222,238}
\definecolor{tssteelblue}{RGB}{0,40,220}
\definecolor{tsorange}{RGB}{255,138,88}
\definecolor{tsblue}{RGB}{23,74,117}
\definecolor{tsforestgreen}{RGB}{21,122,81}
\definecolor{tsyellow}{RGB}{255,185,88}
\definecolor{tsgrey}{RGB}{200,200,200}
\definecolor{main}{RGB}{0,120,2}
\definecolor{seco}{RGB}{230,90,7}%
\definecolor{thid}{RGB}{0,160,152}%
\definecolor{bule}{RGB}{18,29,57}
\definecolor{bablue}{RGB}{248,248,248}
\definecolor{c1}{RGB}{62, 97, 127}
\definecolor{c2}{RGB}{104, 182, 182}
\definecolor{c3}{RGB}{107, 190, 190}
\definecolor{c4}{RGB}{100, 172, 174}
\definecolor{c5}{RGB}{95, 162, 162}
\definecolor{c6}{RGB}{235,244,244}
\definecolor{c7}{RGB}{220,236,236}
\definecolor{c8}{RGB}{209,230,231}
%======================================================================
% 设置日期显示格式为yyyy-mm-dd
\def\twodigits#1{\ifnum#1<10 0\fi\the#1}
\renewcommand{\today}{\number\year-\twodigits\month-\number\day}
%======================================================================
\setcounter{secnumdepth}{4}  % 章节编号深度 (part 对应 -1)
\setcounter{tocdepth}{3}     % 目录深度 
\newcolumntype{d}[1]{D{.}{.}{#1}}% or D{.}{,}{#1} or D{.}{\cdot}{#1}
%======================================================================
\newcommand{\cndash}{\rule{0.0em}{0pt}\rule[0.35em]{1.4em}{0.05em}\rule{0.2em}{0pt}}
\newcommand{\ch}{\titleformat{\chapter}[display]{\centering}{}{-3mm}{\Huge\bfseries}
	\titlespacing{\chapter}{0pt}{0pt}{2\baselineskip}}%用来将需要的章节标题居中
%======================================================================
% 行距缩放因子
\linespread{1.3}
%======================================================================
% 设置名称：目录、表格索引、插图索引
\ctexset{contentsname={\q@contentsname}}
\ctexset{listfigurename={\q@listfigurename}}
\ctexset{listtablename={\q@listtablename}}
\renewcommand{\lstlistingname}{\q@value@listingname}
%======================================================================
% 定制章节样式
\titleformat{\chapter}[display]{\flushleft}{
	\begin{tikzpicture}
	\node[anchor=south west] (chap) at (0.1,1.3){\fontsize{96pt}{96pt}\bfseries\thechapter};
	\path [left color=C1,right color=C2] (0,1) rectangle (\textwidth,0);
	\path(0,-0.2); 
	\end{tikzpicture} 
}{-3mm}{\Huge\bfseries}
\titlespacing{\chapter}{0pt}{0pt}{2\baselineskip}
%======================================================================
% section级样式设置
\ctexset{section={
	format={\color{tssteelblue}\large\bfseries},
	afterskip={1.0ex \@plus .2ex},
	}
}
%======================================================================
% subection级样式设置
\ctexset{subsection={
	format={\color{tssteelblue}\bfseries\normalsize},
	indent={0\ccwd},
	afterskip={1.0ex \@plus .2ex},
	}
}
%======================================================================
% subsubection级样式设置
\ctexset{subsubsection={
	format={\color{tssteelblue}\bfseries\small},
	indent={0\ccwd},
	afterskip={1.0ex \@plus .2ex},
	}
}
%======================================================================
% 设置item条目的索引符号为bullet
\renewcommand{\labelitemi}{\ensuremath{\RHD}}
%======================================================================
% 设置图片载入路径及扩展名
\graphicspath{{fig/}{figure/}{figures/}{logo/}{logos/}{graph/}{graphs}}
\DeclareGraphicsExtensions{.pdf,.eps,.png,.jpg,.jpeg}
%======================================================================
% 设置图片的标题样式
\DeclareCaptionFont{kaishu}{\kaishu}
\captionsetup{format=plain,labelformat=simple,labelsep=space,justification=centering,font={small,kaishu}}
\captionsetup[sub]{font=footnotesize}
\DeclareCaptionOption{bi-first}[]{
    \def\tablename{\q@tablename}
    \def\figurename{\q@figurename}
}
\DeclareCaptionOption{bi-second}[]{
    \def\tablename{Table}
    \def\figurename{Figure}
}
\captionsetup[bi-first]{bi-first}
\captionsetup[bi-second]{bi-second}
%======================================================================
% Set fontnote font size in threeparttable
\appto\TPTnoteSettings{\footnotesize}
%======================================================================
% 浮动参数
\renewcommand{\textfraction}{0.15}
\renewcommand{\topfraction}{0.85}
\renewcommand{\bottomfraction}{0.65}
\renewcommand{\floatpagefraction}{0.60}
%======================================================================
% 公式的编号为"x.y"的形式，图、表的编号为"x-y"的形式
\renewcommand{\theequation}{\arabic{chapter}.\arabic{equation}}
\renewcommand{\thefigure}{\arabic{chapter}--\arabic{figure}}
\renewcommand\p@subfigure{\thefigure}
\renewcommand{\thetable}{\arabic{chapter}--\arabic{table}}
\AtBeginDocument{\renewcommand{\thelstlisting}{\arabic{chapter}--\arabic{lstlisting}}}
%======================================================================
% 使用enumitem宏包配制列表环境
\setlist{nosep}  % 紧凑间距
\setlist*{leftmargin=*}  % 列表和段落头对齐
\setlist[1]{labelindent=\parindent} % Only the level 1
%======================================================================
% 设置宏包 listings/lstlistings
\lstset{tabsize=4, %
  frame=shadowbox,  %把代码用带有阴影的框圈起来
  commentstyle=\color{red!50!green!50!blue!50},  %浅灰色的注释
  rulesepcolor=\color{red!20!green!20!blue!20},  %代码块边框为淡青色
  keywordstyle=\color{blue!90}\bfseries,  %代码关键字的颜色为蓝色，粗体
  showstringspaces=false,  %不显示代码字符串中间的空格标记
  stringstyle=\ttfamily,  % 代码字符串的特殊格式
  keepspaces=true,   %
  breakindent=22pt,  %
  numbers=left,  %左侧显示行号
  stepnumber=1,  %
  numberstyle=\tiny,  %行号字体用小号
  basicstyle={\footnotesize\ttfamily},  %
  showspaces=false,  %
  flexiblecolumns=true,  %
  breaklines=true,  %对过长的代码自动换行
  breakautoindent=true, %
  breakindent=4em,  %
  aboveskip=1em,  %代码块边框
  fontadjust,
  captionpos=t,
  framextopmargin=2pt,framexbottommargin=2pt,abovecaptionskip=-9pt,belowcaptionskip=9pt,
  xleftmargin=4em,xrightmargin=4em,  % 设定listing左右的空白
  texcl=true,
  % 设定中文冲突，断行，列模式，数学环境输入，listing数字的样式
  extendedchars=false,columns=flexible,mathescape=true
  numbersep=-1em
}
%======================================================================
% Setting Package siunitx
\sisetup{detect-all} % Detecting fonts
%======================================================================
% 定制定理、定义、观察、规则、keypoint环境
 \tcbset{
 	commondef/.style={
 		fontupper=\kaishu,
 		lower separated=false,
 		coltitle=white,
 	%	colback=yellow!20,
 	    colback=c6,
 		fonttitle=\heiti\bfseries,
 		enhanced,
 		breakable,
 		top=10pt,
 		left=8pt,
 	%	bottom=6pt,
 		before skip=8pt,
 		attach boxed title to top left={yshift=-0.11in,xshift=0.15in},
 		boxed title style={boxrule=0pt,colframe=white,arc=0pt,outer arc=0pt},
	 },
	 commonpron/.style={
 		fontupper=\kaishu,
 		lower separated=false,
 		coltitle=white,
 		colback=yellow!20,
 		fonttitle=\heiti\bfseries,
 		enhanced,
 		breakable,
 		top=10pt,
 		left=8pt,
 	%	bottom=6pt,
 		before skip=8pt,
 		attach boxed title to top left={yshift=-0.11in,xshift=0.15in},
 		boxed title style={boxrule=0pt,colframe=white,arc=0pt,outer arc=0pt},
 	},
 	commonthm/.style={
 		fontupper=\kaishu,
 		lower separated=false,
 		coltitle=white,
 		colback=c7,
 		fonttitle=\heiti\bfseries,
 		enhanced,
 		breakable,
 		top=10pt,
 	%	bottom=6pt,
 		before skip=8pt,
 		attach boxed title to top left={yshift=-0.11in,xshift=0.15in},
 		boxed title style={boxrule=0pt,colframe=white,arc=0pt,outer arc=0pt},
 	},
 	commonlem/.style={
 		fontupper=\kaishu,
 		lower separated=false,
 		coltitle=white,
 		colback=gray!20,
 		fonttitle=\heiti\bfseries,
 		enhanced,
 		breakable,
 		top=10pt,
 		%	bottom=6pt,
 		before skip=8pt,
 		attach boxed title to top left={yshift=-0.11in,xshift=0.15in},
 		boxed title style={boxrule=0pt,colframe=white,arc=0pt,outer arc=0pt},
 	},
 	common/.style={
 		fontupper=\kaishu,
 		lower separated=false,
 		coltitle=white,
 		colback=c8,
 		fonttitle=\heiti\bfseries,
 		enhanced,
 		breakable,
 		top=10pt,
 	%	bottom=6pt,
 		before skip=8pt,
 		attach boxed title to top left={yshift=-0.11in,xshift=0.15in},
 		boxed title style={boxrule=0pt,colframe=white,arc=0pt,outer arc=0pt},
 	},
 	defstyle/.style={
 		commondef,
 		colframe=tsblue,  
 		colbacktitle=tsblue, 
 		overlay unbroken and last={\node[anchor=south east, outer sep=6pt] at (\textwidth-width,0) {\textcolor{tsblue}{$\davidsstar$}}; },
 		separator sign none
	 },
	 pronstyle/.style={
		commondef,
		colframe=seco,  
		colbacktitle=seco, 
		overlay unbroken and last={\node[anchor=south east, outer sep=6pt] at (\textwidth-width,0) {\textcolor{seco}{$\clubsuit$}}; },
		separator sign none
	},
 	thmstyle/.style={
 		common,
 		colframe=main,  
 		colbacktitle=main, 
 		overlay unbroken and last={\node[anchor=south east, outer sep=6pt] at (\textwidth-width,0) {\textcolor{main}{\textleaf}}; },
 		separator sign none
 	},
 	propstyle/.style={
 		commonthm,
 		colframe=thid,  
 		colbacktitle=thid, 
 		overlay unbroken and last={\node[anchor=south east, outer sep=6pt] at (\textwidth-width,0) {\textcolor{thid}{$\Join$}}; },
 		separator sign none
 	},
     lemstyle/.style={
 	commonlem,
 	colframe=bablue,  
 	colbacktitle=seco, 
 	overlay unbroken and last={\node[anchor=south east, outer sep=6pt] at (\textwidth-width,0) {\textcolor{seco}{$\diamondsuit$}}; },
 	separator sign none
    },
 }

\newtcbtheorem[auto counter,number within=chapter]{mydef}{定义}{defstyle}{def} %定义环境,计数器名tcb@cnt@mydef

\newaliascnt{counterpropsition}{tcb@cnt@mydef} % 复制mydef环境的计数器，用作mythm环境的计数器
\numberwithin{counterpropsition}{chapter}
\newtcbtheorem[use counter=counterpropsition,number within=chapter]{mypron}{命题}{pronstyle}{pron} %命题环境

\newaliascnt{countertheorem}{tcb@cnt@mydef} % 复制mydef环境的计数器，用作mythm环境的计数器
\numberwithin{countertheorem}{chapter}
\newtcbtheorem[use counter=countertheorem,number within=chapter]{mythm}{定理}{thmstyle}{thm} %定理环境

\newaliascnt{counterproperty}{tcb@cnt@mydef} % 复制mydef环境的计数器，用作myprop环境的计数器
\numberwithin{counterproperty}{chapter}
\newtcbtheorem[use counter=counterproperty,number within=chapter]{myprop}{性质}{propstyle}{prop}  %性质环境

\newaliascnt{counterlemma}{tcb@cnt@mydef} % 复制mydef环境的计数器，用作mylem环境的计数器
\numberwithin{counterlemma}{chapter}
\newtcbtheorem[use counter=counterlemma,number within=chapter]{mylem}{引理}{lemstyle}{lem} %引理环境

\newaliascnt{counterremark}{tcb@cnt@mydef} % 复制mydef环境的计数器，用作remark环境的计数器
\newtheorem{remarksty}[counterremark]{{\makebox[0pt][r]{\scriptsize\color{red!90}\textdbend\quad}\textbf{注}}} %带编号注
\newenvironment{remark}   
{\begin{remarksty}} {\end{remarksty}}
%======================================================================
% 设置页眉与页脚样式
\newcommand\q@fancyhead{\small\kaishu}
\def\markboxwidth{0.75\textwidth}
\pagestyle{fancy}
\fancyhf{} 
\fancyhead[LE,RO]{\sffamily\normalsize\thepage}  %在奇数页的右上角显示页码，偶数页的左上角显示页码
\fancyhead[LO]{\nouppercase{\q@fancyhead\rightmark}} % 在奇数页的左侧显示小节名
\fancyhead[RE]{\nouppercase{\q@fancyhead\leftmark}}  % 在偶数页的右侧显示章名  
\renewcommand{\headrulewidth}{0.5pt} 
\addtolength{\headheight}{2.5pt} 
\renewcommand{\footrulewidth}{0pt} 
\fancypagestyle{plain}{\fancyhead{}\renewcommand{\headrulewidth}{0pt}} 
%======================================================================
% Removes the header from odd empty pages at the end of chapters
\makeatletter
\renewcommand{\cleardoublepage}{
	\clearpage\ifodd\c@page\else
	\hbox{}
	\vspace*{\fill}
	\thispagestyle{empty}
	\newpage
	\fi}
\makeatother
%======================================================================
%定制example环境
\makeatletter
\RequirePackage[framemethod=default]{mdframed} 
% Example box
\newmdenv[skipabove=5pt,
skipbelow=7pt,
rightline=false,
leftline=true,
topline=false,
bottomline=false,
backgroundcolor=sthlmGreen!5,
linecolor=sthlmGreen,
innerleftmargin=0.5pt,
innerrightmargin=0pt,
innertopmargin=0pt,
innerbottommargin=0pt,
leftmargin=0cm,
rightmargin=0cm,
linewidth=1pt]{exaBox}

\newtheoremstyle{blacknumexa}% Theorem style Example
{5pt}% Space above
{5pt}% Space below
{\kaishu}% Body font
{} % Indent amount
{\small\bf\kaishu\color{sthlmGreen}}% Theorem head font
{\;}% Punctuation after theorem head
{0.25em}% Space after theorem head
{\small\sffamily\color{sthlmGreen}\thmname{#1}\nobreakspace\thmnumber{\@ifnotempty{#1}{}\@upn{#2}}% Theorem text (e.g. Theorem 2.1)
	\thmnote{\nobreakspace\the\thm@notefont\heiti\color{sthlmGreen}\nobreakspace(#3)}}% Optional

\newaliascnt{counterexample}{tcb@cnt@mydef} %复制mydef环境的计数器,给example环境使用
\theoremstyle{blacknumexa}
\newtheorem{exampleT}[counterexample]{例}
\newenvironment{example}{\begin{exaBox}\begin{exampleT}}{\hfill{\color{sthlmGreen}}\end{exampleT}\end{exaBox}} %example环境
%======================================================================
%定制例子中的横线
\newcommand{\cGreen}[1]{{\color{sthlmGreen}{#1}}}
\newcommand{\soln}[1]{\par\vspace{1.5pt}\makebox[5pt]{\begin{tikzpicture}[overlay]
		\node at (-15pt,0pt){\textcolor{sthlmGreen}{\ding{45}}};\end{tikzpicture}}\cGreen{\noindent\hrulefill\vskip 1pt}}
\makeatother
%======================================================================
% 前言
\makeatletter
\newenvironment{pre}{
	\ch\chapter{\q@pre}{}}{}
%======================================================================
% 概览
\newenvironment{overview}{
\ch\chapter{\q@overviewname}{}}{}
%======================================================================
% 设置目录
\renewcommand\tableofcontents{%
  \cleardoublepage
  \pdfbookmark[0]{\contentsname}{toc}
  \chapter*{\centerline{\contentsname}}
  \@mkboth{\MakeUppercase\contentsname}{\MakeUppercase\contentsname}%
  \@starttoc{toc}%
}
\addtocontents{toc}{\let\string\CTEX@spaceChar\relax}
%======================================================================
% 设置交叉引用样式
\labelformat{counterexample}{\text{例}~#1}
\labelformat{tcb@cnt@mydef}{\text{定义}~#1}
\labelformat{countertheorem}{\text{定理}~#1}
\labelformat{counterpropsition}{\text{命题}~#1}
\labelformat{counterproperty}{\text{性质}~#1}
\labelformat{counterlemma}{\text{引理}~#1}
\labelformat{counterremark}{\text{注}~#1}
\labelformat{equation}{\text{式}~(#1)}
\labelformat{figure}{\text{图}~#1}
\labelformat{table}{\text{表}~#1}
\labelformat{chapter}{\@firstoftwo{\CTEX@prechapter\chinese{chapter}\CTEX@postchapter}{#1}}
\labelformat{section}{(#1)~\text{节}}
\labelformat{subsection}{(#1)~\text{节}}
\labelformat{subsubsection}{(#1)~\text{节}}
%======================================================================
% 汉化证明环境
\renewcommand{\proofname}{\bfseries\q@label@proof}  
%======================================================================
\endinput
