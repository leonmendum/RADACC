\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{estposter}[2015/06/30 The EST labs poster class (based on ICM poster class)]

\LoadClass[portrait,a3]{a0poster}

\RequirePackage{fontspec}
\RequirePackage{xunicode}
\defaultfontfeatures{Mapping=tex-text}

\setmainfont{Arial-Regular}

%\RequirePackage{ngerman}
\RequirePackage[german,ngerman]{babel}
\RequirePackage{graphicx}
\RequirePackage{color} 
\RequirePackage{xcolor}
\RequirePackage[absolute]{textpos}
\RequirePackage{xkeyval}
\RequirePackage{wasysym}
\RequirePackage{ccicons}
\RequirePackage{rotating}
\RequirePackage{tikz}

%%% HDA color model %%% don't use rgb colors while printing 
%\definecolor{HDA_darkgreen}{rgb}{.254,.333,0}
%\definecolor{HDA_green}{rgb}{.549,.666,0}
%\definecolor{HDA_lightgreen}{rgb}{.901,.941,.784}
%\definecolor{HDA_red}{rgb}{.647,.058,.098}
%\definecolor{HDA_darkred}{rgb}{.392,.039,.058}
%\definecolor{HDA_darkviolet}{rgb}{.372,0,.313}
%\definecolor{HDA_darkblue}{rgb}{.098,.176,.392}
%\definecolor{HDA_yellow}{rgb}{1.000,.803,0}
%\definecolor{HDA_orange}{rgb}{.901,.568,.098}
%\definecolor{HDA_violet}{rgb}{.666,.372,.607}
%\definecolor{HDA_blue}{rgb}{.372,.607,.803}
%\definecolor{HDA_lightred}{rgb}{.941,.901,.882}
%\definecolor{HDA_lightyellow}{rgb}{1.000,.960,.784}
%\definecolor{HDA_lightviolet}{rgb}{.960,.901,1.000}
%\definecolor{HDA_lightblue}{rgb}{.882,.921,1.000}

%%% HDA color model %%% use cmyk colors while printing 
\definecolor{HDA_darkgreen}{cmyk}{.71,.35,1.00,.50}
\definecolor{HDA_green}{cmyk}{.50,.13,1.00,.06}
\definecolor{HDA_lightgreen}{cmyk}{.09,.0,.25,.06}
\definecolor{HDA_red}{cmyk}{.18,1.00,1.00,.18}
\definecolor{HDA_darkred}{cmyk}{.0,1.00,.71,.71}
\definecolor{HDA_darkviolet}{cmyk}{.50,1.00,.0,.50}
\definecolor{HDA_darkblue}{cmyk}{1.00,.71,.0,.50}
\definecolor{HDA_yellow}{cmyk}{.0,.18,1.00,.0}
\definecolor{HDA_orange}{cmyk}{0,.50,1.00,.06}
\definecolor{HDA_violet}{cmyk}{.35,.71,.0,.06}
\definecolor{HDA_blue}{cmyk}{.71,.25,.0,.0}
\definecolor{HDA_lightred}{cmyk}{.0,.06,.06,.09}
\definecolor{HDA_lightyellow}{cmyk}{.0,.09,.25,.0}
\definecolor{HDA_lightviolet}{cmyk}{.06,.13,.0,.0}
\definecolor{HDA_lightblue}{cmyk}{.13,.06,.0,.0}
\definecolor{radacc_darkblue}{RGB}{17,41,74}
\definecolor{radacc_lightGray}{RGB}{201,208,221}
\definecolor{radacc_blue}{RGB}{27, 59, 99}
\definecolor{radacc_lightBlue}{RGB}{26, 50, 83} 
\definecolor{radacc_lightererBlue}{RGB}{40, 84, 137}
\definecolor{radacc_lighterGray}{RGB}{217, 217, 217}


\definecolor{HDA_gray_100}{gray}{0} % black 100%
\definecolor{HDA_gray_71}{gray}{.29}
\definecolor{HDA_gray_50}{gray}{.5}	
\definecolor{HDA_gray_35}{gray}{.65}
\definecolor{HDA_gray_25}{gray}{.75}
\definecolor{HDA_gray_18}{gray}{.82}
\definecolor{HDA_gray_13}{gray}{.87}
\definecolor{HDA_gray_9}{gray}{.91}
\definecolor{HDA_gray_6}{gray}{.94}
\definecolor{HDA_gray_0}{gray}{1} %white

\newcommand{\stdtextcolor}{\color{HDA_gray_0}}
\newcommand{\stdpagecolor}{\pagecolor{HDA_red}}

%% options processing %%

%% define color of text %%
\DeclareOptionX{textcolor}{\renewcommand{\stdtextcolor}{\color{#1}}}

%% define color of page %%
\DeclareOptionX{pagecolor}{\renewcommand{\stdpagecolor}{\pagecolor{#1}}}

%% draw grid %%
\DeclareOptionX{drawgrid}{\AtEndOfClass{\RequirePackage[colorgrid,texcoord]{eso-pic}}}

\ProcessOptionsX\relax

\newcommand{\customtextblockstyle}[2]{%
\stdtextcolor\fontsize{#1}{#2}\selectfont%
}

\newcommand{\textblockstyle}{%
\customtextblockstyle{16pt}{22pt}%
}

\newcommand{\titleblockstyle}{%
\bf\customtextblockstyle{80pt}{85pt}%
}

\newcommand{\subtitleblockstyle}{%
\customtextblockstyle{50pt}{53pt}%
}

\newcommand{\footnoteblockstyle}{%
\customtextblockstyle{5pt}{5pt}%
}


%%% placegraphics %%%
% arg1: width of block
% arg2: horizontal (x) location
% arg3: vertical (y) location 
% arg4: graphics file
\newcommand{\placegraphics}[4]{%
\begin{textblock}{#1}(#2,#3) 
{\includegraphics[width=\textwidth]{#4}}
\end{textblock}}

%%% the title %%%
% arg1: title
\newcommand{\titleblock}[1]{%
\begin{textblock}{26}(2,7) 
\titleblockstyle #1
\end{textblock}}

%%% the subtitle %%%
% arg2: subtitle
\newcommand{\subtitleblock}[1]{%
\begin{textblock}{26}(2,10) 
\subtitleblockstyle #1
\end{textblock}}

%%% the est logo %%%
% arg1: logo graphics file
\newcommand{\estlogo}[1]{\placegraphics{10}{20}{0.3}{#1}}

%%% the fbi logo %%%
% arg1: logo graphics file
\newcommand{\fbilogo}[1]{\placegraphics{6}{2}{39}{#1}}

%%% publication date block %%%
\newcommand{\publicationblock}{%
\begin{textblock}{11.5}(18,41.3)
\footnoteblockstyle
\begin{flushright}
Ver\"offentlicht am \publishdate \ {}- \publisher
\end{flushright}
\end{textblock}}

%% intitialize texblock layout %%
\setlength{\TPHorizModule}{10mm} 
\setlength{\TPVertModule}{\TPHorizModule} 
\textblockorigin{0mm}{0mm} % start everything near the top-left corner 
\setlength{\parindent}{0pt}

\AtBeginDocument{\stdpagecolor}

%% EOF
