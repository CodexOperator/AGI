---
id: doc:draft-presentation-deck-v1
mint_id: 1b7b6e432698486ba1707a68ad0f1c8a
type: doc
parents:
  - goal:g5.4.3.1
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
title: "DRAFT presentation deck v1 (arm A, basic workflow) -- privacy-scanned graph copy of the class rough draft, for the council's full pass"
town: core
---
# DRAFT — presentation deck v1, graph copy (arm A: basic workflow)

DRAFT. Every on-screen line marked '% OWNER c:<id>' and every spoken note line opening 'OWNER (c:...)' is the owner's; every other line is an agent's (labelled "cleaned up rough draft written by AI:" where it proposes wording). The council's full pass reads THIS version (council [decision] alive 09:53:15Z 11-10, goal:g5.4.3.1.1).

source sha256: 30c850e0a5b62554547091628a2ac246ac283e95d355bd24ad2a45f12a6bb192
copied: 2026-11-10T10:39:58Z
'% OWNER' lines: 44
removals: [elided: course] x4 lines (127, 128, 410, 411), [elided: person] x1 line (410), [withheld: verbal-only] x0
owner lines a removal touched: none (127 and 410 are agent paraphrases of owner asides, labelled so; 128 and 411 are agent suggestions)
submitted bytes: rough-draft-v1 = the PRIVATE deck as built (the owner's Drive agi/class-presentation/rough-draft-v1/), not this copy

## deck.tex (copy)
````latex
% DRAFT -- deck/deck.tex -- beamer 16:9 skeleton (v2.1). EVERY on-screen line and every spoken line is the owner's:
% each slot is [OWNER WRITES: what the line must do] (+ guiding questions in the \note). The agent's parts are the
% visuals, the clip plumbing, the chart specs and the cites. Nothing the owner keeps verbal-only is written anywhere in this file (owner, c:2763ec818294),
% speaker notes included; check-owner.sh (F1+F2 of goal:g5.4.3.1) reads it.
% Build: latexmk -pdf deck.tex  (from deck/, after `make videos posters` one level up; see ../README.md)
% Clip pattern: poster + \movie (pdfpc / some Acrobat) + "watch online" + "open local file" + QR, then a fallback
% frame of per-beat stills (\only<n>) that works in every viewer. Missing files render as labelled placeholders.
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{default}
\usefonttheme{professionalfonts}
\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{newunicodechar}\newunicodechar{·}{\textperiodcentered}\newunicodechar{≈}{$\approx$}\newunicodechar{→}{$\rightarrow$}\newunicodechar{—}{---}\newunicodechar{–}{--}
\usepackage{graphicx,tikz,multimedia,hyperref}
\usetikzlibrary{shapes.geometric,positioning,arrows.meta,calc}
\tikzset{alt/.code args={<#1>#2#3}{\alt<#1>{\pgfkeysalso{#2}}{\pgfkeysalso{#3}}}} % beamer-aware style switch
\IfFileExists{qrcode.sty}{\usepackage{qrcode}\newif\ifqr\qrtrue}{\newif\ifqr\qrfalse}
\graphicspath{{../}{../posters/}{../figures/}}

% ---------- palette (storyboard.md, light surface) ----------
\definecolor{ink}{HTML}{0B0B0B}\definecolor{ink2}{HTML}{52514E}\definecolor{edge}{HTML}{9AA4B2}
\definecolor{goal}{HTML}{2A78D6}\definecolor{idea}{HTML}{EDA100}\definecolor{hyp}{HTML}{6250D6}
\definecolor{exp}{HTML}{1BAF7A}\definecolor{verdict}{HTML}{EB6834}\definecolor{moral}{HTML}{E87BA4}
\definecolor{vision}{HTML}{008300}\definecolor{serious}{HTML}{E34948}
\setbeamercolor{normal text}{fg=ink}\setbeamercolor{structure}{fg=goal}\setbeamercolor{frametitle}{fg=ink}
\setbeamerfont{frametitle}{size=\LARGE,series=\bfseries}\setbeamerfont{title}{size=\Huge,series=\bfseries}
\setbeamertemplate{navigation symbols}{}\setbeamertemplate{footline}[frame number]
\setbeamersize{text margin left=1.2cm,text margin right=1.2cm}

% ---------- DRAFT watermark on every page (tune once compiled) ----------
\usebackgroundtemplate{\tikz[overlay]\node[rotate=28,scale=7,text=gray,opacity=0.10]at(0.5\paperwidth,-0.5\paperheight){DRAFT};}
\setbeameroption{hide notes}   % pdfpc: \setbeameroption{show notes on second screen=right}

% ---------- numbers: one place to refresh (charts.md) ----------
\newcommand{\asof}{as of 11-07, refresh pending}
\newcommand{\nNodes}{5{,}842}\newcommand{\nCommits}{$\sim$25{,}400}\newcommand{\nLands}{426}\newcommand{\nLandsDay}{22}
\newcommand{\linkbase}{https://REPLACE-ME.example/agi-talk}   % unlisted playlist or repo folder; one edit

% ---------- helpers ----------
\newcommand{\slot}[1]{{\color{ink2}[OWNER WRITES: #1]}}
\newcommand{\maybefig}[2][\textwidth]{\IfFileExists{#2}{\includegraphics[width=#1]{#2}}%
  {\fbox{\parbox[c][0.36\textheight][c]{\dimexpr#1-2\fboxsep-2\fboxrule\relax}{\centering\color{ink2}\footnotesize\itshape animation goes here (rendered video ships with the package)\\[2pt]\ttfamily\scriptsize\detokenize{#2}}}}}
\newcommand{\vclip}[2]{\begin{center}%  #1 stem, #2 clip label.  0.405 = 9/16 x 0.72
  \IfFileExists{../videos/#1.mp4}{\movie[width=0.72\textwidth,height=0.405\textwidth,poster,showcontrols]%
      {\maybefig[0.72\textwidth]{posters/#1.png}}{../videos/#1.mp4}}{\maybefig[0.72\textwidth]{posters/#1.png}}\\[2pt]
  {\footnotesize #2\quad\href{\linkbase/#1.mp4}{\underline{watch online}}\quad\href{run:../videos/#1.mp4}{\underline{open local file}}}%
  \hfill\ifqr\qrcode[height=1.3cm]{\linkbase/#1.mp4}\else\fbox{\footnotesize QR}\fi\end{center}}
\newcommand{\steps}[1]{\only<1>{\maybefig{posters/#1_step1.png}}\only<2>{\maybefig{posters/#1_step2.png}}%
  \only<3>{\maybefig{posters/#1_step3.png}}\only<4->{\maybefig{posters/#1_step4.png}}}% 4-step fallback
\newcommand{\tmbox}[1]{\fbox{\parbox[c][2.1cm][c]{0.4\textwidth}{\centering\ttfamily\small [TM: #1]}}}
\tikzset{every node/.style={font=\small},n/.style={draw=#1,line width=1pt,rounded corners=3pt,minimum height=7mm,inner sep=4pt,text=ink},
  e/.style={draw=edge,line width=0.9pt},card/.style={draw=edge,fill=edge!15,minimum width=9mm,minimum height=4mm,inner sep=0}}
% v3, S3 org build: od = a person dot, oe = a thin link; \orgrow{x}{y}{example name}{bar fill 0..1} writes the name and
% its bar to the right of a 14 x 11 mm mini-graph whose lower-left corner is (x,y) mm. The fill is ILLUSTRATIVE (one
% level per group, set by hand): research-f found no measured quality score for any of these structures.
\tikzset{od/.style={circle,fill=ink2,inner sep=0pt,minimum size=1.4mm},oe/.style={draw=edge,line width=0.5pt}}
\newcommand{\orgrow}[4]{\node[anchor=west,align=left,text width=22mm,font=\tiny,text=ink,inner sep=0pt] at (#1+16,#2+7.5) {#3};
  \draw[edge,line width=0.4pt] (#1+16,#2+0.5) rectangle (#1+36,#2+2.3);\fill[edge!70] (#1+16,#2+0.5) rectangle ({#1+16+20*#4},#2+2.3);}
% v5, S7 flow-of-work build (workflow: owner 11-10): seat = a role on the chart, dir = a director's seat (narrow, two
% lines), act = a seat acting on this click, tnode = a tree node (colour = type), tok = the hand-off arrow, twig = a thin
% branch, shoot = this round's growth (it thickens on click 8 = step 7, when the Prime lands it).
\tikzset{seat/.style={draw=ink2,line width=0.8pt,rounded corners=2pt,fill=white,minimum width=19mm,minimum height=6.5mm,inner sep=1pt,font=\scriptsize,text=ink},
  dir/.style={minimum width=14.5mm,minimum height=8mm,align=center,font=\tiny},
  act/.style={draw=goal,line width=1.8pt},
  tnode/.style={draw=#1,line width=0.9pt,rounded corners=1.5pt,fill=white,minimum height=4.4mm,inner sep=1.2pt,font=\tiny,text=ink},
  tok/.style={draw=goal,line width=1.6pt,-{Stealth[length=2.4mm]}},twig/.style={draw=edge,line width=0.9pt},
  shoot/.style={draw=edge,line width=0.9pt,alt={<8->{draw=ink,line width=1.8pt}{}}}}

\title{AGI: Advanced Graph Interface}                          % OWNER c:b16c08f739c5
\subtitle{Attempting to give long-term awareness to ephemeral agents}  % OWNER c:b16c08f739c5
\author{the owner}\date{Tue 11-11 · class rough draft}

\begin{document}

% ===== S1 hook (0:25) =====
\begin{frame}[plain]
  \vspace{0.6cm}{\usebeamerfont{title}Can you prove to me you achieved anything?}\\[4pt] % OWNER c:2763ec818294
  \vclip{hf_threshold}{C0 · HyperFrames · 8 s}
  \note{OWNER'S NOTE (theirs): no insult intended. Literally: can you give a formula where x crossing 80\% officially means goal y is achieved? Then examples that seem easy until you ask who decides how x is calculated, how it is measured, how good the instruments are.\\
  cleaned up rough draft written by AI: And no, I am not trying to insult anyone. I mean it literally: can you give me a formula that says ``once x crosses 80\%, I have officially achieved goal y''? [spoken, for the note above; your verbatim line is in owner-lines.md] \\
  cleaned up rough draft written by AI: [empty slot, the examples] Start easy: ``I ran five miles.'' ``I passed with an 80.'' Then pull the thread: who decided 80 was the line? Who wrote the test? How well does the test measure the thing it claims to measure? \\
  OWNER (c:31a2e2b871f1), the plant, spoken: Or in other words, why even the most basic things we are used to doing every day - like say putting together a presentation - aren't as simple as they first appear.\\
  cleaned up rough draft written by AI: In other words: why even the most basic things we do every day, like putting together a presentation, are not as simple as they first appear. [spoken, the plant] \\
  Bookend: the same bar returns on the last slide (C7).}
\end{frame}
\begin{frame}[plain]\steps{hf_threshold}\end{frame}
% ===== S1b title card (owner, chunk 2): the name after the hook =====
\begin{frame}[plain]
  \titlepage
  % v3 visual plant (review-fable52.md #4): a WORDLESS chain, the silhouette of the reveal clip C6. Shapes follow the
  % glyph table (goal, goal, doc, post, doc, the chunks; side branch = fuel). No ids here: S9 puts them on.
  % \titlepage ends on a \vfill, so the chain sits under the title block, near the bottom of the frame.
  \par\centering
  \begin{tikzpicture}[x=13mm,y=1mm,pl/.style={draw=edge,line width=0.9pt,inner sep=0pt}]
    \node[pl,rounded corners=2pt,minimum width=8mm,minimum height=4mm] (a) at (0,0) {};
    \node[pl,rounded corners=2pt,minimum width=8mm,minimum height=4mm] (b) at (1,0) {};
    \node[pl,minimum width=4mm,minimum height=5.5mm] (c) at (2,0) {};
    \node[pl,circle,minimum size=5mm] (d) at (3,0) {};\fill[edge] (d) circle (0.7mm);
    \node[pl,draw=goal,line width=1.3pt,minimum width=4mm,minimum height=5.5mm] (e) at (4,0) {};
    \node[pl,dashed,rounded corners=2pt,minimum width=8mm,minimum height=4mm] (f) at (5,0) {};
    \node[pl,dashed,semicircle,minimum size=3mm] (g) at (4,-8) {};
    \draw[e] (a)--(b);\draw[e] (b)--(c);\draw[e] (c)--(d);\draw[e] (d)--(e);\draw[e,dashed] (e)--(f);\draw[e,dashed] (e)--(g);
    % v4 (graph shape everywhere): sideways growth, LEFT -> RIGHT, allowed where space demands it. Two roots (morals) sit left
    % of a ground line, the trunk (vision, a diamond) just right of it; the chain then grows rightward as before. Still wordless.
    % Clip C6 draws the same chain growing UPWARD; this is its silhouette turned on its side.
    \node[pl,circle,draw=moral,minimum size=3mm] (ra) at (-1.5,3.5) {};\node[pl,circle,draw=moral,minimum size=3mm] (rb) at (-1.5,-3.5) {};
    \node[pl,diamond,draw=vision,minimum size=4.5mm] (tr) at (-0.75,0) {};
    \draw[ink2,line width=1.2pt] (-1.15,-6.5) -- (-1.15,6.5);
    \draw[e] (ra)--(tr);\draw[e] (rb)--(tr);\draw[e] (tr)--(a);
  \end{tikzpicture}\par\vspace{5mm}
  \note{OWNER'S NOTE (theirs, chunk 2): just like a human, an agent could really benefit from a sort of flowchart to show it what's going on and what it should do next.}
  \note{cleaned up rough draft written by AI: An attempt to give short-lived AI agents long-term awareness [on screen, the subtitle: ``ephemeral'' is jargon for this room]}
  \note{cleaned up rough draft written by AI: Just like a person, an AI agent works better with a kind of flowchart: one that shows what is going on and what to do next. (An agent, here, is an AI model that carries out a task on its own, step by step.) [spoken; the bracket defines ``agent'' on first use]}
  \note{AI flag (not a rewording): most of this room will read ``AGI'' as artificial general intelligence. If the double meaning is intended, one spoken clause should say so.}
\end{frame}

% ===== S2 problem (0:40) =====
\begin{frame}{How do we get multiple agents to collaborate reliably?} % OWNER c:4b5d4abae03e
  \only<1-2>{\vclip{hf_context}{C1 · HyperFrames · 9 s · one agent, one context window}} % v3: C1 leaves when C1b enters
  \only<2>{\vfill A single agent \emph{could} get it done, usually} % OWNER c:pending-tap (context-management caveats: spoken only)
  \only<3>{\vclip{mn_timelines}{C1b · manim · 10 s · one agent vs many, with throttle dials · illustrative}} % owner-approved visual
  \note{OWNER (c:pending-tap): Let's say you want to take a video game like (anyone got one in mind? what's one of your favorites?) and you want to figure out the code behind it and then rewrite the whole game in Go while optimizing it to run even faster, or rewrite it so it runs in a web browser on your phone. \\
  cleaned up rough draft written by AI: Say you want to take a video game (anyone have a favorite?), work out the code behind it, and rewrite the whole thing in another programming language, Go, so that it runs even faster. Or rewrite it so it runs in a web browser on your phone. [spoken] \\
  OWNER (c:pending-tap), the point to make here: technically a single agent could do this, but over a way longer period of time. We want to be able to both meaningfully speed up how long it takes to finish a given task, but also be able to control how fast and how much any individual agent does to avoid wasted effort. \\
  cleaned up rough draft written by AI: Technically, one agent could do this. It would just take far longer. We want two things: to cut the time a task takes, and to control how fast and how much each agent does, so that no effort is wasted. [spoken] \\
  Fallback if the room names no game: Doom ("Can it run Doom?"), owner-approved. \\
  OWNER (c:pending-tap), the open loop, spoken: So it makes sense, if you were told to go rewrite Doom, and assigned a room of people, you'd get it done pretty fast. If you were only assigned a single person, it would probably take you a while. But think about being in that room sitting in front of a group of highly-paid, highly-capable, and highly-intelligent software engineers. How do you even organize everyone? Just say `Okay team we're rewriting Doom in Go, good luck!' then go sit on your phone while they do everything themselves? Can someone like you or me who don't know nearly as much about computers or coding even provide effective leadership in an unfamiliar territory? \\
  cleaned up rough draft written by AI: It makes sense: told to rewrite Doom and given a room full of people, you would finish fast. Given one person, it would take a while. But picture yourself at the front of that room, facing a group of highly capable software engineers. How do you even organize them? Do you say ``Okay team, we are rewriting Doom in Go, good luck!'' and then sit on your phone while they do everything? Can someone like you or me, who knows far less about computers and code, lead well in unfamiliar territory? [spoken, the open loop] \\
  Agent paraphrase of an owner aside (c:2a8dd9b727c1), not verbatim: aimed at the humanities professors present: the AI program is part of a new humanities course too, [elided: course], which lets humanities get in on the STEM/software fun via LLM intelligence-hierarchy flattening. \\
  cleaned up rough draft written by AI: A nod to the humanities professors here: [elided: course] is a humanities course too. These AI models flatten the ladder of technical expertise, so the humanities get to join the software fun. [spoken aside; ``LLM intelligence-hierarchy flattening'' is jargon] \\
  Cites: Liu et al. 2023 Lost in the Middle, 56.1\% closed-book vs 53.8\% mid-context (GPT-3.5 era). Hong et al. 2025 Context Rot, 18 LLMs degrade as input grows (vendor report).}
\end{frame}
\begin{frame}{How do we get multiple agents to collaborate reliably?\hfill{\small\color{ink2}fallback}}\steps{hf_context}\end{frame} % OWNER c:4b5d4abae03e
\begin{frame}[plain]\steps{mn_timelines}\end{frame} % v3: C1b fallback stills (untitled, so no owner line is repeated)

% ===== S3 why organize (1:15): clip, then three beginner tools as an overlay build =====
\begin{frame}{How do we turn nebulous needs into achievable goals?} % OWNER c:pending-tap
  \vclip{manim_channels}{C2 · manim · 8 s}
\end{frame}
% ----- S3 v3, PROPOSED clip C2b (review-fable52.md #6): these frames exist only once videos/mn_needs.mp4 is rendered -----
\newif\ifneedsclip\IfFileExists{../videos/mn_needs.mp4}{\needscliptrue}{\needsclipfalse}
\ifneedsclip
\begin{frame}[plain]\vspace{0.4cm}\vclip{mn_needs}{C2b · manim · 8 s · illustrative}\end{frame}
\begin{frame}[plain]\steps{mn_needs}\end{frame}
\fi
% ----- S3 click-build: the experience chain (owner 11-10; illustrative bars, NO data) -----
\begin{frame}{How do we turn nebulous needs into achievable goals?} % OWNER c:pending-tap
  \centering
  % v3 fix: the click number is written out per role (v2 put \the\numexpr inside an overlay spec and inside a node
  % name, and needed calc); edges go node to node. Same clicks as the note: 2-5 = one role + its bar, 6 = the axis.
  % Bars: ILLUSTRATIVE heights (3/8/15/24), one flat tint, no axis, no numbers; the tag shows as soon as a bar does.
  % Loop variables are multi-letter on purpose: \i, \k, \r, \a, \b, \c are text accents and \ht is a TeX primitive.
  \begin{tikzpicture}[x=33mm,y=1mm]
    \foreach \pos/\clk/\barh/\role in {0/2/3/{customer},1/3/8/{salesman \textbar{} website},2/4/15/{product manager \textbar{} middle manager},3/5/24/{coder}}{
      \uncover<\clk->{
        \fill[edge!45] (\pos-0.2,0) rectangle (\pos+0.2,\barh);
        \node[n=ink2,align=center,text width=24mm,font=\scriptsize] (r\pos) at (\pos,-9) {\role};}}
    \foreach \ea/\eb/\clk in {0/1/3,1/2/4,2/3/5}{\uncover<\clk->{\draw[e,-{Stealth}] (r\ea) -- (r\eb);}}
    \uncover<2->{\node[font=\tiny,text=ink2,anchor=east] at (3.4,27) {illustrative, not measured};}
    \uncover<6->{\draw[e,-{Stealth}] (-0.4,-20) -- (3.4,-20);
      \node[font=\small,text=ink] at (1.5,-24) {less professional experience \hfill\hspace{4mm}$\longrightarrow$\hspace{4mm} more professional experience building software}; % OWNER c:pending-tap
      }
  \end{tikzpicture}
  \note{Click 1 = title; clicks 2-5 = one role and its bar each (no role is explained, they just exist); click 6 = the arrow and its label. OWNER (c:pending-tap), the point, spoken: so yes that is the whole point of business: connect people with zero or a tiny bit of experience at doing or making service a or item x with the people who have the most useful experience and can apply it the best. Answers S2's open loop (``can someone like you or me provide effective leadership?''). Bars are ILLUSTRATIVE heights, no numbers; a real figure would need a source.}
  \note{cleaned up rough draft written by AI: So yes, that is a big part of what a business is for: connecting people who have little or no experience making a thing with the people who have the most, and who can apply it best. [spoken; ``the whole point of business'' is a sweeping claim, softened here]}
  \note{cleaned up rough draft written by AI: less experience $\longrightarrow$ more experience building software [on screen, the axis label: says ``professional'' and ``experience'' once less]}
\end{frame}
% ----- S3 continues: why structure -----
\begin{frame}{How do we turn nebulous needs into achievable goals?} % OWNER c:pending-tap
  % v3 ORG BUILD (TikZ, plays in every viewer; it is its own fallback). Click 1 = title only; click 2 = the bad ones,
  % CENTRE; click 3 = the good ones, RIGHT; click 4 = the beginner ones, LEFT (the order of the spoken line below).
  % On screen: example names only. Every bar is ILLUSTRATIVE, one hand-set level per group; cites are in the 2nd \note.
  \centering
  \begin{tikzpicture}[x=1mm,y=1mm]
    \path (0,-4) rectangle (130,48); % fixed bounding box: nothing shifts between clicks
    \uncover<2->{% ---------- the bad ones, centre column (x = 47) ----------
      \node[font=\tiny,text=ink2,anchor=east] at (130,-3) {bars: illustrative, not measured};
      \begin{scope}[shift={(47,36)}]% a hidden clique of three; the rest only touch the clique (dashed = unofficial)
        \foreach \px/\py/\qx/\qy in {1/9/6/7,12/10/6/7,13/3/8.5/4.5,9/0.5/8.5/4.5,1/1/5/3.5}{\draw[oe,dashed] (\px,\py)--(\qx,\qy);\node[od] at (\px,\py){};}
        \draw[oe,dashed] (6,7)--(8.5,4.5)--(5,3.5)--cycle;
        \foreach \px/\py in {6/7,8.5/4.5,5/3.5}{\node[od] at (\px,\py){};}
      \end{scope}\orgrow{47}{36}{structureless group}{0.2}
      \begin{scope}[shift={(54,23.5)}]% six people, every pair linked
        \foreach \na in {0,...,5}{\foreach \nb in {0,...,5}{\ifnum\na<\nb\relax\draw[oe,line width=0.3pt] (\na*60:5)--(\nb*60:5);\fi}}
        \foreach \na in {0,...,5}{\node[od] at (\na*60:5){};}
      \end{scope}\orgrow{47}{18}{everyone talks to everyone}{0.2}
      \begin{scope}[shift={(47,0)}]% two bosses per worker; the second boss's lines in the serious colour
        \draw[oe] (4,10.5)--(4,2) (10,10.5)--(10,2);
        \draw[oe,draw=serious] (0.7,6.5)--(10,6.5) (0.7,2)--(10,2);
        \foreach \px/\py in {4/10.5,10/10.5,0.7/6.5,0.7/2,4/6.5,10/6.5,4/2,10/2}{\node[od] at (\px,\py){};}
      \end{scope}\orgrow{47}{0}{matrix with conflicting dual bosses}{0.2}}
    \uncover<3->{% ---------- the good ones, right column (x = 94) ----------
      \begin{scope}[shift={(94,36)}]% four stream teams on one platform, one enabling team (dashed)
        \draw[oe,fill=edge!20] (1,1.5) rectangle (13,3.5);
        \foreach \sx in {2,5.3,8.7,12}{\draw[oe] (\sx,8.5)--(\sx,3.5);\node[od] at (\sx,8.5){};}
        \draw[oe,dashed] (12,8.5)--(14,11);\node[od,minimum size=1mm] at (14,11){};
      \end{scope}\orgrow{94}{36}{Team Topologies}{0.85}
      \begin{scope}[shift={(94,18)}]% intent down (thick), information sideways (thin)
        \foreach \sx in {1.5,5.2,8.8,12.5}{\draw[oe,line width=1.2pt] (7,10.5)--(\sx,3);}
        \draw[oe,line width=0.3pt] (1.5,3)--(12.5,3);
        \foreach \sx in {1.5,5.2,8.8,12.5}{\node[od] at (\sx,3){};}\node[od] at (7,10.5){};
      \end{scope}\orgrow{94}{18}{mission command}{0.85}
      \begin{scope}[shift={(94,0)}]% a line of five; every station can reach the one stop-the-line node
        \draw[oe] (1,8.5)--(13,8.5);
        \foreach \sx in {1,4,7,10,13}{\draw[oe,line width=0.3pt] (\sx,8.5)--(7,1.5);\node[od] at (\sx,8.5){};}
        \node[circle,draw=ink2,fill=white,line width=0.5pt,inner sep=0pt,minimum size=1.9mm] at (7,1.5){};
      \end{scope}\orgrow{94}{0}{Toyota Production System}{0.85}}
    \uncover<4->{% ---------- the beginner ones, left column (x = 0) ----------
      \begin{scope}[shift={(7,41.5)}]% one hub, six spokes
        \foreach \na in {0,...,5}{\draw[oe] (0,0)--(\na*60:5);\node[od] at (\na*60:5){};}\node[od] at (0,0){};
      \end{scope}\orgrow{0}{36}{founder hub}{0.55}
      \begin{scope}[shift={(0,18)}]% a strict tree: clear, no sideways links
        \foreach \hx in {2.5,7,11.5}{\draw[oe] (7,10.5)--(\hx,6) (\hx,6)--(\hx-1.4,1.5) (\hx,6)--(\hx+1.4,1.5);
          \node[od] at (\hx,6){};\node[od] at (\hx-1.4,1.5){};\node[od] at (\hx+1.4,1.5){};}\node[od] at (7,10.5){};
      \end{scope}\orgrow{0}{18}{functional hierarchy}{0.55}
      \begin{scope}[shift={(9,5.5)}]% one small ring, fed through one backlog (the square)
        \draw[oe] (0:4) \foreach \na in {1,...,5}{ -- (\na*60:4)} -- cycle;
        \foreach \na in {0,...,5}{\node[od] at (\na*60:4){};}
        \draw[oe] (-8.3,0)--(-4,0);\node[od] at (-8.3,0){};
        \node[draw=ink2,fill=white,line width=0.5pt,inner sep=0pt,minimum size=1.7mm] at (-6.2,0){};
      \end{scope}\orgrow{0}{0}{single Scrum team}{0.55}}
  \end{tikzpicture}
  \note{V3 ORG BUILD, cites (research-f; say none of this on screen). No source gives a quality score per structure, so every bar is illustrative. Bad: Freeman 1972 (structureless group, hidden elite); Brooks 1975 (every pair linked: the count is arithmetic, print no figure); Davis and Lawrence 1978 (matrix PATHOLOGIES: they did not say a matrix is always bad, hence ``conflicting dual bosses''). Beginner: Mintzberg 1980 (simple structure; machine bureaucracy); Scrum Guide 2020 (UNVERIFIED in this pass). Good: Skelton and Pais 2019 (Team Topologies); US Army ADP 6-0 (mission command; hard to copy, per its historians); Ohno 1978/1988 (Toyota Production System, UNVERIFIED in this pass: check before saying). One comparative study to keep in your pocket: Doty, Glick and Huber 1993 found ``closer to the ideal type = more effective'' NOT supported, while fit to context predicted 24\% of the variance in effectiveness (abstract only read).}
  \note{OWNER (c:pending-tap), spoken over the org build (clicks: bad slide in to the MIDDLE, then good on the RIGHT, then beginner on the LEFT): There about infinite ways to throw people at a problem, but over time we have figured out that some *click: the bad ones* don't work at all, some *click: the good ones* work really well, and some *click: the beginner ones* are perfect for people just getting into organizing other people. \\
  cleaned up rough draft written by AI: There are endless ways to throw people at a problem. Over time we have learned that some *click: the bad ones* tend to fail, some *click: the good ones* tend to work really well, and some *click: the beginner ones* are a good fit for people just starting to organize others. [spoken; fixes ``There about''; ``tend to'' because no source scores these structures, see the cites note] \\
  AI fact flag (not a rewording): ``don't work at all'' and ``work really well'' are stronger than the sources. Research-f found no measured quality score for any structure, and the one comparative study (Doty, Glick and Huber 1993, abstract only) found fit to context mattered, not closeness to an ideal type. \\
  VISUAL (owner 11-10, spec pending research-f): per group, several textbook examples, each a small node-graph of its structure + a bar for org quality (illustrative unless sourced). \\
  Cites: Brooks 1975 (wording verified; pairwise count n(n-1)/2 is arithmetic). Cemri et al. 2025 MAST: ~44\% of tagged failures are specification / system-design (sum of per-mode shares). Conway 1968: name it, do not quote it (wording unverified).}
\end{frame}
\begin{frame}{How do we turn nebulous needs into achievable goals?\hfill{\small\color{ink2}fallback}}\steps{manim_channels}\end{frame}

% ===== S4 why the long way (0:50) =====
% beginner tools moved here from S3 (owner 11-10: 'moving it to slide 4 also makes sense'; kept short)
\begin{frame}{When you're first learning about running agent swarms:} % OWNER c:pending-tap
  \centering
  \begin{tikzpicture}[node distance=4mm and 14mm]
    \uncover<1->{\node[n=ink2,minimum width=26mm,minimum height=22mm,align=center](k){};
      \node[card,above left=-8mm and -11mm of k.north]{};\node[card,above left=-13mm and -11mm of k.north]{};
      \node[card,above right=-8mm and -11mm of k.north]{};\node[card,above=-8mm of k.north]{};
      \node[below=1mm of k,align=center]{kanban board\\[1mm]{\footnotesize\color{exp}+ who's doing what}\\{\footnotesize\color{serious}-- no ``why''}};} % OWNER c:pending-tap
    \uncover<2->{\node[n=ink2,right=of k,minimum width=26mm,minimum height=22mm](c){};
      \node[circle,draw=ink2,inner sep=1.5pt,above left=-7mm and -8mm of c.north](f1){};\node[circle,draw=ink2,inner sep=1.5pt,above right=-7mm and -8mm of c.north](f2){};
      \node[circle,draw=ink2,inner sep=1.5pt,above=-16mm of c.north](f3){};\draw[e](f1)--(f2);\draw[e](f1)--(f3);\draw[e](f2)--(f3);
      \node[below=1mm of c,align=center]{code graph\\[1mm]{\footnotesize\color{exp}+ how pieces connect}\\{\footnotesize\color{serious}-- no intent}};} % OWNER c:pending-tap
    \uncover<3->{\node[n=ink2,right=of c,minimum width=26mm,minimum height=22mm](s){};
      \node[circle,draw=ink2,double,inner sep=2.5pt,above=-13mm of s.north](a){};
      \draw[e,-{Stealth}](a.east) arc (-90:200:3.5mm);\node[below=1mm of s,align=center]{self-prompting loop\\[1mm]{\footnotesize\color{exp}+ runs unattended}\\{\footnotesize\color{serious}-- goes off-track}};} % OWNER c:pending-tap
  \end{tikzpicture}
  \note{OWNER (c:pending-tap), little speaking here: the bullets carry it. Bridge, spoken: Each one individually is missing a critical piece of the full picture. A piece which doesn't matter to humans because we know how to fill in one of these pieces if the other two are filled in.}
  \note{cleaned up rough draft written by AI: When you first learn to run many agents at once: [on screen, the title: ``agent swarms'' is jargon]}
  \note{cleaned up rough draft written by AI: Each one, on its own, is missing a critical piece of the picture. People do not notice the gap: give us any two of the pieces and we fill in the third ourselves. [spoken, the bridge]}
  \note{cleaned up rough draft written by AI: A kanban board is a wall of task cards. A code graph is a map of how the parts of a program connect. A self-prompting loop is an agent that keeps handing itself the next instruction. [spoken, new: one gloss per tool, since the three names are jargon here]}
\end{frame}
% ----- S4 venn (owner 11-10): why · decisions · stop point; one circle shaded at a time, then all clear -----
\begin{frame}{When you're first learning about running agent swarms:} % OWNER c:pending-tap
  \centering
  \begin{tikzpicture}[c/.style={draw=ink2,line width=1pt,circle,minimum size=34mm}]
    \def\A{(0,0)}\def\B{(2.2,0)}\def\C{(1.1,-1.9)}
    \only<2>{\fill[goal,opacity=.35] \A circle (17mm);}\only<3>{\fill[idea,opacity=.35] \B circle (17mm);}\only<4>{\fill[verdict,opacity=.35] \C circle (17mm);}
    \node[c] at \A {};\node[c] at \B {};\node[c] at \C {};
    \node at (-0.5,0.4) {why};\node at (2.7,0.4) {decisions};\node at (1.1,-2.6) {stop point}; % OWNER c:pending-tap
  \end{tikzpicture}
  \note{Clicks: 1 three empty circles · 2 why shaded · 3 decisions shaded, why clears · 4 stop point shaded, decisions clears · 5 all clear. As a clip: C3v (storyboard-v3), one semi-quick animation of the same beats.}
\end{frame}
% ----- S4 preview (owner yes, 11-10): the chain, wordless but for node-type names, NO numbers (~3 s); S8 pays it off -----
\begin{frame}[plain]
  \centering\vspace{0.1cm}
  % v4 (graph shape everywhere): the same chain, now growing UPWARD. Morals = the roots under the ground line; vision = the
  % trunk; the chain climbs from the goal to the result. Node-type names only, no numbers (as before).
  \begin{tikzpicture}[x=1mm,y=1mm]
    \draw[ink2,line width=1.2pt] (-45,0) -- (45,0);
    \foreach \rootx in {-12,-4,4,12}{\draw[e] (0,0) -- (\rootx,-5);
      \node[circle,draw=moral,fill=white,line width=1pt,minimum size=3mm,inner sep=0pt] at (\rootx,-6) {};}
    \node[font=\small,text=ink,anchor=west] at (16,-6) {moral};
    \node[n=vision,fill=white](vi) at (0,8){vision};\draw[e,line width=1.6pt] (0,0) -- (vi);
    \node[n=goal](g) at (0,19){goal};\node[n=idea](i) at (0,30){idea};\node[n=hyp](h) at (0,41){hypothesis};
    \node[n=exp](x) at (0,52){experiment};\node[n=verdict](v) at (0,63){result};
    \foreach \nfrom/\nto in {vi/g,g/i,i/h,h/x,x/v}{\draw[e,-{Stealth}](\nfrom)--(\nto);}
  \end{tikzpicture}
  \note{A 3-second flash, no words spoken: ``all this trouble'' in the next title points here. Same chain as S8's funnel (which adds the counts).}
  \note{V4: the chain now climbs from roots (moral) and a trunk (vision) below it: the tree shape used on every later slide.}
\end{frame}
\begin{frame}{The AI's are really good at coding already, why even bother with this?} % OWNER c:pending-tap
  \begin{columns}[T]
  \column{0.47\textwidth}
    \begin{enumerate}
      \item<1-> weaker models % OWNER c:pending-tap
      \\{\footnotesize\color{ink2}Sinha et al. 2025; METR horizon $\sim$7-month doubling. (thin evidence: say so)}
      \item<2-> knowing the stop-point % OWNER c:pending-tap
      \\{\footnotesize\color{ink2}Qu et al. 2026: off-scope 0.0\% $\to$ 17.1\% without a scope statement.}
      \item<3-> repeating others' work % OWNER c:pending-tap
      \\{\footnotesize\color{ink2}Ron et al. 2026: 3-version vote 387 $\to$ 131 failures / 1M tests. Brown et al. 2024: 15.9\% $\to$ 56\%.}
    \end{enumerate}
    \uncover<4->{To be fair, the big models are REALLY smart % OWNER c:pending-tap
      \\{\footnotesize\color{ink2}Yan / Cognition 2025.}}
  \column{0.53\textwidth}
    \only<3>{\vclip{manim_fanout}{C3 · manim · 10 s}}\only<4>{\vclip{mn_triangle}{C3t · manim · 9 s · time · cost · quality, illustrative}}
  \end{columns}
  \note{OWNER (c:pending-tap + 11-10 edits), spoken on click 4: The company behind the autonomous agent Devin, meant to work autonomously start-to-finish, says that splitting work between agents loses shared context, and that one agent is more reliable due to unified context. [triangle clip C3t now has no spoken line: owner to keep or cut] \\
  cleaned up rough draft written by AI: Cognition, the company behind Devin, an AI agent built to work on its own from start to finish, argues that splitting work between agents loses shared context, and that a single agent is more reliable because its context stays in one place. [spoken on click 4; names the company and says ``argues'': this is their published position, not a measurement] \\
  OWNER (c:pending-tap), spoken: We know the AIs today are, to be somewhat humble, probably slightly better than I am at coding. So why even bother having them go through all this trouble? I bet we could ask Einstein the same question. Why bother having to formalize his insight into all these fancy math formulas that people can run in experiments to see if the math matches reality. He could've just said ``its all, like, relative, man'' and moved on with his life. It's because of the golden rule of science: as Adam Savage said, the difference between science and just messing around is writing it down. \\
  cleaned up rough draft written by AI: We know today's AIs are, to be somewhat humble, probably a bit better at coding than I am. So why make them go through all this trouble? We could ask Einstein the same thing: why bother turning his insight into formal math that others can test against reality? He could have just said ``it's all, like, relative, man'' and moved on with his life. The answer is the golden rule of science. As Adam Savage put it: the difference between science and just messing around is writing it down. [spoken; ``its'' to ``it's'', shorter sentences] \\
  cleaned up rough draft written by AI: AIs are already really good at coding. Why even bother? [on screen, the title: 10 words, was 13; ``AI's'' to ``AIs''; two sentences, no comma splice] \\
  Slots, one per click. Q1 (title now filled): Q2: what did a small local model do when you gave it a long job? Q3: what did an agent build that you never asked for? Q4: when did two independent builds disagree and which was right? \\
  cleaned up rough draft written by AI: [empty slot, reason 1] Smaller models lose the thread on long jobs sooner than big ones. A written structure lets them finish work they could not hold on their own. (The evidence for this one is thin: say so.) \\
  cleaned up rough draft written by AI: [empty slot, reason 2] Without a written scope, agents overreach. In one 2026 study, one coding agent's out-of-scope actions went from 0.0\% to 17.1\% once the scope statement was removed. \\
  cleaned up rough draft written by AI: [empty slot, reason 3] Independent attempts catch each other's mistakes. In one 2026 study, a three-version vote cut failures from about 387 to about 131 per million tests, although the failures that remain cluster where the task itself is ambiguous. \\
  cleaned up rough draft written by AI: [empty slot, the triangle clip C3t] Every setup is a trade between three things. Push toward one corner and the other two give. \\
  AI fact flags (not rewordings): (1) the Savage line is usually quoted as ``the only difference between screwing around and science is writing it down''. No research file checks the wording or who said it first, and ``golden rule of science'' is your own label: find the source before attributing it. (2) ``One agent is more reliable due to unified context'' is a paraphrase; the verified quote (Yan 2025) is that running multiple agents in collaboration ``only results in fragile systems'', and it says ``in 2025''. (3) ``Meant to work autonomously start-to-finish'' is in no research file. (4) Reason 3 can be heard two ways, wasted duplicate work or useful double-checking; the cite printed under it supports only the second. \\
  Cite details: Qu et al. 2026 Claude Code paired scenarios, McNemar p=2.4e-4; Ron et al. 2026 means 387.44 and 130.99, failures correlate on ambiguous spec parts (Knight and Leveson 1986); Brown et al. 2024 needs a verifier to pick the sample.}
\end{frame}
\begin{frame}{The AI's are really good at coding already, why even bother with this?\hfill{\small\color{ink2}fallback}}\steps{manim_fanout}\end{frame}

% ===== S5 solution (0:45): TikZ overlay build; pre-trains node / parent / goal =====
% ===== S5a OPTIONAL, skippable: from harness tricks to the graph (owner idea 11-10) =====
\begin{frame}[label=harness]{\slot{the tools, then their natural conclusion, $\le$ 12 words}}
  \only<1>{\vclip{mn_harness_b1}{C3b · manim · beat 1 of 4 · reset · skippable}}% v3: one file per click
  \only<2>{\vclip{mn_harness_b2}{C3b · manim · beat 2 of 4 · compaction · skippable}}%
  \only<3>{\vclip{mn_harness_b3}{C3b · manim · beat 3 of 4 · fork · skippable}}%
  \only<4>{\vclip{mn_harness_b4}{C3b · manim · beat 4 of 4 · the graph · skippable}}
  \only<1>{\begin{tikzpicture}[overlay,remember picture]\node[draw=ink2,fill=white,rotate=-3,dashed,inner sep=6pt,font=\large,anchor=north east] at ($(current page.north east)+(-8mm,-14mm)$) {``A single agent \emph{could} get it done, usually''};\node[font=\tiny,text=ink2,anchor=north east] at ($(current page.north east)+(-9mm,-26mm)$) {from slide 2};\end{tikzpicture}} % OWNER line reused verbatim (c:pending-tap), owner 11-10: cutout/quote of slide 2
  \hfill\hyperlink{solution}{\beamerbutton{skip}}
  \note{OWNER (c:pending-tap), MOVED HERE FROM S2 (owner 11-10), with the slide-2 cutout on click 1: technically even one agent could do it with enough context resets: so some way for it to reset its context and start a fresh session independently, or with the help of the human user. There's also things like continuous context compaction, or session forking, that have been receiving attention. [sources: research-d, pending] \\
  cleaned up rough draft written by AI: Technically, even one agent could do it, given enough fresh starts: some way to clear its working memory and begin a new session, on its own or with the user's help. Other tricks have been getting attention too, like continuously summarizing that memory (compaction), or splitting one session into two (forking). [spoken; ``There's also things'' fixed, the two terms glossed] \\
  OWNER's idea (theirs, c:pending-tap): Anthropic's ``effective harness'' (progress file + git history for a fresh session) taken to its natural conclusion: a whole graph of git histories LLMs can browse, and a graph of thoughts they can pick up from. Beats you can skip through: 1 reset + handoff note (Anthropic 2025-11-26) · 2 compaction (MemGPT 2023; OptMem, early-stage software) · 3 session forking (Claude Code /branch, docs only) · 4 the graph: every session's handoff is a node, every node has parents. Cites: research-d. No number on ``much slower'' (none measured).}
  \note{cleaned up rough draft written by AI: Anthropic's recipe for long-running agents is a progress file plus the project's change history, so that a fresh session can pick up where the last one stopped. Take that to its natural conclusion and you get a graph: every change history there to browse, every thought there to pick up from. [a spoken version of the idea note; ``harness'' and ``git'' are jargon here]}
  \note{cleaned up rough draft written by AI: [empty slot, the title] One agent, three memory tricks, and where they lead}
  \note{AI fact flag (not a rewording): the same Anthropic post says ``compaction isn't sufficient'' (research-d). Resets with a hand-off file are well supported; compaction alone is not. No figure exists for ``much slower'': give none.}
\end{frame}
\begin{frame}[plain]\steps{mn_harness}\end{frame} % v3: C3b fallback stills; the skip button jumps past this too
\begin{frame}[label=solution]{What if we just graph the thoughts and their thinkers together} % OWNER c:pending-tap
  \centering
  \begin{tikzpicture}[node distance=9mm and 4mm]
    % v4 (graph shape everywhere): sideways growth, LEFT -> RIGHT (the crew chart below needs the height). The root (moral)
    % sits left of a ground line, the trunk (vision) right of it, then the chain as before; node distance 7mm -> 4mm to fit.
    \node[circle,draw=moral,line width=1pt,minimum size=3.5mm,inner sep=0pt](mo){};\node[font=\tiny,text=ink2,below=0.5mm of mo]{moral};
    \node[diamond,draw=vision,line width=1pt,minimum size=5.5mm,inner sep=0pt,right=7mm of mo](vi){};\node[font=\tiny,text=ink2,below=0.5mm of vi]{vision};
    \draw[ink2,line width=1.2pt] ($(mo.east)!0.5!(vi.west)+(0,-6mm)$) -- ($(mo.east)!0.5!(vi.west)+(0,6mm)$);
    \draw[e,<-,>=Stealth](mo)--(vi);
    \node[n=goal,right=of vi](g){goal};\draw[e,<-,>=Stealth](vi)--(g);
    \node[n=idea,right=of g,circle,rounded corners=0](i){idea};
    \node[n=hyp,right=of i,regular polygon,regular polygon sides=6,rounded corners=0,inner sep=1pt](h){hyp.};
    \draw[e,<-,>=Stealth](g)--node[above,font=\scriptsize,text=ink2]{parent}(i);\draw[e,<-,>=Stealth](i)--(h);
    \uncover<2->{
      \node[n=exp,right=of h,rounded corners=0](x){experiment};
      \node[n=verdict,right=of x,regular polygon,regular polygon sides=3,rounded corners=0,inner sep=0pt](v){\scriptsize v.};
      \node[n=ink2,right=of v,trapezium,rounded corners=0](m){mvp};
      \node[n=ink2,right=of m,star,star points=5,rounded corners=0,inner sep=0pt](o){\scriptsize o.};
      \draw[e,<-,>=Stealth](h)--(x);\draw[e,<-,>=Stealth](x)--(v);\draw[e,<-,>=Stealth](v)--(m);\draw[e,<-,>=Stealth](m)--(o);
      }
    \uncover<3->{
      \node[n=ink2,below=16mm of i](p){prime};
      \node[n=ink2,below left=7mm and 9mm of p](m1){master};\node[n=ink2,below right=7mm and 9mm of p](m2){master};
      \node[n=ink2,below=7mm of m1](d1){director};\node[n=ink2,below=7mm of m2](d2){director};
      \node[n=ink2,right=5mm of d2,dashed](k){kids};
      \draw[e](p)--(m1);\draw[e](p)--(m2);\draw[e](m1)--(d1);\draw[e](m2)--(d2);\draw[e,dashed](d2)--(k);
      \node[n=ink2,right=10mm of m2](cn){council}; \draw[e](p)--(cn); \draw[ink2,line width=.8pt,<->,>=Stealth](m2)--node[above,font=\tiny,text=ink2]{side by side}(cn); % bicameral: council beside master (owner 11-10)
      \begin{scope}[every node/.style={font=\tiny,text=ink2,align=left,text width=34mm}]
        \node[left=2mm of p]{decides when to go and when to stop with the help of the human user. Also does initial setup.}; % OWNER c:pending-tap
        \node[left=2mm of m1]{decides who is doing what.}; % OWNER c:pending-tap
        \node[right=2mm of cn]{figures out how we should do it, and whether how we did it matches how we should've done it}; % OWNER c:pending-tap
        \node[left=2mm of d1]{Figures out what to do next right now}; % OWNER c:pending-tap
        \node[below=1mm of k,text width=22mm]{do the thing a director assigned.}; % OWNER c:pending-tap
      \end{scope}}
  \end{tikzpicture}
  \note{OWNER (c:pending-tap), spoken on click 3 (the hierarchy): My idea so far has been to organize everyone roughly like this. This doesn't include everyone, but it includes every `level' of work management I needed to make it work the smoothest so far. \\
  cleaned up rough draft written by AI: So far, my idea has been to organize everyone roughly like this. It leaves some roles out, but it shows every level of management I have needed to keep things running smoothly. [spoken on click 3] \\
  cleaned up rough draft written by AI: What if we just graph the thoughts and their thinkers together? [on screen, the title: adds the question mark] \\
  cleaned up rough draft written by AI: Prime: decides when to go and when to stop, together with the human user; also does the initial setup. $\cdot$ master: decides who does what. $\cdot$ council: decides how we should do it, then checks that what we did matches. $\cdot$ director: decides what to do next. $\cdot$ kids: do the task a director assigns. [on screen, the five role lines: tightened, same verb throughout] \\
  AI fact flag (not a rewording): in the system's own docs a ``parent'' agent sits between a director and its kids (a director never sends work to a kid directly), and the council's check comes after the master's gate and before the Prime lands the change. Your spoken ``this doesn't include everyone'' covers the first; be ready if someone asks. \\
  Cites: Anthropic 2024 "predefined code paths"; Yan 2025 "share full agent traces"; Hong et al. 2023 MetaGPT SOPs.}
\end{frame}
% ----- S5b node anatomy (owner 11-10): bullets left; a REAL node right, goal:g5.4.3.2 (the paper): foreshadows S9 -----
\begin{frame}{What if we just graph the thoughts and their thinkers together} % OWNER c:pending-tap
  \begin{columns}[T]
  \column{0.42\textwidth}
    A node has a few key pieces: % OWNER c:pending-tap
    \begin{itemize}
      \item<2-> \textbf{\color{goal}parents} -- tells us where it is % OWNER c:pending-tap
      \item<3-> \textbf{\color{hyp}thought} -- tells us why it is % OWNER c:pending-tap
      \item<4-> \textbf{\color{exp}body} -- tells us what it is % OWNER c:pending-tap
    \end{itemize}
  \column{0.56\textwidth}
    \begin{tikzpicture}[font=\ttfamily\scriptsize,every node/.style={anchor=north west,inner sep=2pt,text width=62mm}]
      \node[draw=ink2,line width=.8pt,rounded corners=3pt,minimum height=50mm,text width=64mm](card) at (0,0) {};
      \node at (1mm,-1mm) {.agi/nodes/goal/g5.4.3.2.md};
      \node[alt=<2>{fill=goal!25}{fill=goal!6}] at (1mm,-6mm) {id: goal:g5.4.3.2\\parents:\\\ \ - goal:g5.4.3};
      \node at (1mm,-18mm) {title: "G5.4.3.2: The class paper after the presentation, good enough to publish as a long-form blog post ..."};
      \node[alt=<4>{fill=exp!25}{fill=exp!6}] at (1mm,-30mm) {\#\# Target end-state\\1. A class paper in the owner's own final wording ...\\2. Fit to publish as a long-form blog post};
      \node[alt=<3>{fill=hyp!25}{fill=hyp!6}] at (1mm,-44mm) {THOUGHT: v1, meme-master 11-10, DRAFT for the council's placement ...};
    \end{tikzpicture}
  \end{columns}
  \note{OWNER (c:pending-tap), spoken: together these turn a bunch of files into a graph without having to draw any actual lines or nodes or put together anything. Just let AI read the files and they will build the graph in their own mind which is the only place it actually needs to exist. I do have tools to make it easier to read many files at once though as a form of AI-optimized graph. \\
  cleaned up rough draft written by AI: Together, these turn a pile of files into a graph, without anyone drawing a single line or box. Let the AI read the files and it builds the graph in its own head, which is the only place the graph needs to exist. I do have tools that make many files easier to read at once: a kind of AI-optimized view of the graph. [spoken] \\
  cleaned up rough draft written by AI: parents: where it is $\cdot$ thought: why it is $\cdot$ body: what it is [on screen, the three bullets: drops the repeated ``tells us''; ``parents tells'' does not agree] \\
  cleaned up rough draft written by AI: A node is one file: one recorded thought. [spoken, new: defines ``node'' before the three bullets] \\
  The card is a real node, trimmed: goal:g5.4.3.2, the paper you still owe; it returns in S9's reveal (foreshadowing, owner 11-10). Its excerpts are the node's own text, quoted as an exhibit.}
\end{frame}

% ===== S6 humans give morals, vision, goals: the corporate parallel (0:35) =====
\begin{frame}{Leadership is a job} % OWNER c:pending-tap
  {\large How do we bridge the gap between potential capability and actual execution?}\par\medskip % OWNER c:pending-tap
  \vclip{hf_morals}{C5 · HyperFrames · 9 s · values poster $\to$ moral $\to$ vision $\to$ goal}
  \only<2->{\par\smallskip{\large Morals are shared cornerstones}} % OWNER c:pending-tap
  \note{OWNER (c:pending-tap), spoken, before the poster clip: This sets up the fact that humans have had books and speeches and whole careers built around speakers and writers and coaches teaching other humans how to lead. Everything is some kinda big systems optimization: block out noisy info and narrow in your tunnel vision on useful signal. Now we're trying to automate that process which itself is a big-systems problem as is AI as a whole. So if humans have made space for leadership as a career, and even teaching leadership as a career, why do we think AI won't need expert leaders? \\
  cleaned up rough draft written by AI: People have built whole careers on this: books, speeches, coaches, all teaching other people how to lead. Much of it is one big systems problem: block out the noise and focus on the useful signal. Now we are trying to automate that, which is a big systems problem of its own, like AI as a whole. So if we have made room for leadership as a career, and even for teaching leadership as a career, why would we think AI will not need expert leaders? [spoken, before the poster clip] \\
  cleaned up rough draft written by AI: How do we bridge the gap between potential and execution? [on screen: 10 words, was 12] \\
  OWNER (c:pending-tap), spoken as the poster appears: every company has some sort of catchy acronym, slogan, or mantra [poster shows real ones, AWS first; list verified in research-g]. These are meant to give us something to hold on to anytime we are unsure of a decision we need to make. They aren't any sort of achievable goal or task, quite the opposite actually. They are vague in a very concrete sort of way on purpose - to limit your decision constructively rather than destructively. They're saying that if you're gonna do something, make sure you do it like this (or basically don't bother doing it at all). \\
  cleaned up rough draft written by AI: Most big companies have some catchy acronym, slogan or mantra. They give us something to hold on to whenever we are unsure about a decision. They are not goals or tasks you can finish; quite the opposite. They are vague on purpose, in a very concrete way: they narrow your choices constructively, not destructively. They say: if you are going to do something, do it like this, or do not bother. [spoken, as the poster appears; ``every company'' softened] \\
  OWNER (c:pending-tap), spoken on ``Morals are shared cornerstones'': Morals are these shared cornerstones that let everyone stay on the same page as far as how we are making decisions and allowing decisions to go through via council votes. Modifying those would let agents decide to focus on something completely outside what the human user wanted to focus on and could include sensitive religious or medical preferences such as if they were building a website for a church. \\
  cleaned up rough draft written by AI: Morals are the shared cornerstones. They keep everyone on the same page about how decisions get made, and about which decisions pass a council vote. If agents could rewrite them, they could drift toward something the human user never asked for. Morals can also carry sensitive preferences, religious or medical ones for example: think of a system building a website for a church. [spoken; the second sentence of the original had no clear subject] \\
  Agent paraphrase of an owner aside (c:24cce6461b83), not verbatim: a nod to [elided: course] and the other humanities faculty, the [elided: person] included: leadership, communications, law, biology... all things the humanities teach here. \\
  cleaned up rough draft written by AI: A nod to [elided: course] and to the humanities faculty: leadership, communications and law are all taught here. [spoken aside; see flag 4 below] \\
  Slots: [OWNER WRITES: the corporate parallel: core values, a unified vision, mantras and acronyms, in your words] Q: which mantra from a job stuck, and why? · [OWNER WRITES: why agents never write the top] · optional [OWNER WRITES: one real example you can vouch for]. \\
  cleaned up rough draft written by AI: [empty slot, why agents never write the top] Agents can grow everything above the ground. The roots are the one thing they never touch: only the human writes the morals. \\
  AI note: the slot ``one real example you can vouch for'' needs your own experience, so no draft is offered. The ``corporate parallel'' slot looks filled by your mantra passage above. \\
  AI fact flags (not rewordings): (1) kaizen means continuous improvement (Toyota Way 2001, research-g). Growing a bonsai and pruning it is your own picture of it: say ``like kaizen'', not ``kaizen is''. (2) AWS lists six pillars today; five was true until December 2021 (research-g). (3) Google's ``Don't be evil'' was not read on an official page in research-g, and the press reports say it moved from the preface to the last line in 2018, not that it was removed: ``former motto'' may overstate it. (4) Biology is not usually counted among the humanities: check the aside before saying it to that faculty. \\
  Facts: only morals are parentless; moral $\to$ vision $\to$ goal; the six morals and G1--G7 are live node ids. OWNER (chunk 2b): go with the values poster dissolving into moral $\to$ vision $\to$ goal; the Toyota kaizen parallel is KEY: kaizen is the graph's growth process, grow the bonsai and prune the useless carefully so only the useful survives (clip C5 ends on a prune beat). Real examples, ALL UNVERIFIED in this pass (check before saying): Amazon Leadership Principles; Netflix culture memo; The Toyota Way. Not on screen.}
\end{frame}
\begin{frame}{Leadership is a job\hfill{\small\color{ink2}fallback}}\steps{hf_morals}\end{frame}

% ===== S7 walkthrough (1:20) =====
\begin{frame}{Let the graph grow} % OWNER c:pending-tap
  \vclip{manim_tree}{C4 · manim · 12 s}
  \note{OWNER (c:c083f191f98d), spoken, kept as is (owner 11-10): okay so for the first step we have the brainstorm session with the more powerful model that creates a goal bundle to add to the town board. (I know that isn't how it is this season but that is the intent). *click: the top-level goals G1-G7 fade in above the goal bundle node* these bundles are linked to our goals which live above them and we so we can think of this tree we are growing. \\
  OWNER DECISION (11-10, option a): when speaking, say the goals live BELOW the bundle (roots-tree: goals sit nearer the roots). \\
  cleaned up rough draft written by AI: Okay, step one: a brainstorm session with the most capable model produces a bundle of goals, and that bundle goes up on the town board, our shared task board. (That is the intent; this season it does not run exactly that way.) *click: the top-level goals G1-G7 fade in* Each bundle links back to our top-level goals, the main branches, so we can think of all of this as a tree we are growing. [spoken; fixes ``and we so we''; ``which live above them'' becomes ``links back to'', because in the roots-tree the goals now sit BELOW the bundle, nearer the trunk] \\
  Slots, one per beat (owner-brief script, the intended flow, not exactly this season's): [beat 1: brainstorm with the stronger model makes a goal bundle on the town board] · [beat 2: G1--G7 fade in above; the bundle links up to them] · [beat 3: "the tree we are growing"] · [beat 4: idea] · [beat 5: hypothesis + falsifier, experiment] · [beat 6: verdict, then mvp / outcome or why it failed] · [beat 7, SKIP IF OVER: done = goals met, checked against the vision, new goals or ask]. Optional: [the 20-s input to output one-liner from v1, or cut].}
  \note{V4 NOTE (stale after v5: the flow is now the owner's 9 steps): clip C4 is re-shaped into the roots-tree: morals under the ground line, vision as the trunk, G1--G7 as the main branches, new growth upward at one tip, one side branch clipped (kaizen). On click 2 the goals fade in BELOW the bundle. The walkthrough's remaining beats are now the flow-of-work build after the fallback frame, one click per step; its eleven draft lines are in that frame's notes.}
\end{frame}
\begin{frame}{Let the graph grow\hfill{\small\color{ink2}fallback: one click = one beat}}
  \only<1>{\maybefig{posters/manim_tree_step1.png}}\only<2>{\maybefig{posters/manim_tree_step2.png}}%
  \only<3>{\maybefig{posters/manim_tree_step3.png}}\only<4>{\maybefig{posters/manim_tree_step4.png}}%
  \only<5>{\maybefig{posters/manim_tree_step5.png}}\only<6->{\maybefig{posters/manim_tree_step6.png}}
\end{frame}
% ----- S7 v5, THE FLOW OF WORK (workflow corrected by the owner, owner 11-10): after the walkthrough, ONE CLICK PER STEP,
% steps 0..8 = clicks 1..9. LEFT = the role chart (human, Prime, council and SM side by side under the Prime, the four
% directors in a row under SM). RIGHT = the roots-tree, growing the nodes each step produces. Labels are role names and
% node-type names only (plus G1..G7 and the one arrow label of step 8).
% The manim clip C4w (src/manim/mn_workflow.py) shows the same nine steps with a moving hand-off token; its frame exists
% only once videos/mn_workflow.mp4 is rendered. The TikZ build below is the fallback and plays in every viewer.
\newif\ifworkclip\IfFileExists{../videos/mn_workflow.mp4}{\workcliptrue}{\workclipfalse}
\ifworkclip
\begin{frame}[plain]\vspace{0.4cm}\vclip{mn_workflow}{C4w · manim · nine steps · the flow of work}\end{frame}
\fi
\begin{frame}[plain]
  % Click k+1 = step k (0..8): nine clicks. Per step: the acting seat gets a thick blue border, ONE \only draws that
  % step's hand-off, and the tree gains that step's nodes (\uncover: they stay). Untitled, so no title line is repeated.
  \centering
  \begin{tikzpicture}[x=1mm,y=1mm]
    \path (2,0) rectangle (136,80); % fixed bounding box: nothing shifts between clicks
    % ---------- LEFT: the role chart (council BESIDE SM; the four directors in a row under SM) ----------
    \node[seat,alt={<1>{act}{}}] (hu) at (37,75) {human};
    \node[seat,alt={<1,8>{act}{}}] (pr) at (37,62) {Prime};
    \node[seat,alt={<6,9>{act}{}}] (sm) at (24,47) {SM};
    \node[seat,alt={<7,9>{act}{}}] (co) at (50,47) {council};
    \node[seat,dir,alt={<2>{act}{}}] (dg) at (9.5,27) {director-\\goals};
    \node[seat,dir,alt={<3,9>{act}{}}] (ds) at (25,27) {director-\\science};
    \node[seat,dir,alt={<4>{act}{}}] (dn) at (40.5,27) {director-\\general};
    \node[seat,dir,alt={<5>{act}{}}] (dr) at (56,27) {director-\\review};
    \draw[twig] (hu)--(pr);\draw[twig] (pr)--(sm);\draw[twig] (pr)--(co);\draw[twig,<->,>=Stealth] (sm)--(co);
    \foreach \dname in {dg,ds,dn,dr}{\draw[twig] (sm)--(\dname);}
    % the hand-off of each step: ONE \only per step, 0..8 (owner 11-10)
    \only<1>{\draw[tok] (hu)--(pr);}                                                                  % 0 human + Prime: the goal bundle
    \only<2>{\draw[tok,-] (pr)--(sm);\draw[tok] (sm)--(dg);}                                          % 1 director-goals (drawn along the chart's lines)
    \only<3>{\draw[tok] (dg.south) to[bend right=50] (ds.south);}                                     % 2 director-science
    \only<4>{\draw[tok] (ds.south) to[bend right=50] (dn.south);}                                     % 3 director-general
    \only<5>{\draw[tok] (dn.south) to[bend right=50] (dr.south);\draw[tok] (dr)--(sm);}               % 4 director-review, then back to SM
    \only<6>{\draw[tok,-] (9.5,47.2) -- (10.6,46) -- (12.8,48.8);}                                    % 5 SM checks it again (a check mark by SM)
    \only<7>{\draw[tok] (sm)--(co);}                                                                  % 6 council
    \only<8>{\draw[tok] (co)--(pr);}                                                                  % 7 Prime: the final hand-off
    \only<9>{\draw[tok,dashed] ([yshift=-2mm]co.west) -- ([yshift=-2mm]sm.east);                      % 8 send-back (example): council -> SM -> director-science
      \draw[tok,dashed] ([xshift=3mm]sm.south) -- ([xshift=3mm]ds.north);
      \node[font=\tiny,text=goal,fill=white,inner sep=0.5pt] at (49,39.6) {send back via SM};
      \foreach \sname in {ds,dn,dr,sm,co,pr}{\fill[white] (\sname.north east) circle[radius=1.9mm]; % the icon: it can happen at every step
        \draw[goal,line width=0.7pt,-{Stealth[length=1.2mm]}] ([xshift=1.3mm]\sname.north east) arc[start angle=0,end angle=280,radius=1.3mm];}}
    % ---------- RIGHT: the roots-tree as it stands before the round (the visions are the trunk) ----------
    \draw[ink2,line width=1.2pt] (70,9) -- (136,9); % the ground line
    \foreach \rootx in {92,98,104,110,116}{\draw[twig] (104,9) -- (\rootx,4.2);
      \node[circle,draw=moral,fill=white,line width=0.9pt,inner sep=0pt,minimum size=2.6mm] at (\rootx,3) {};}
    \node[font=\tiny,text=ink,anchor=west] at (119,3) {moral};
    \foreach \vnum/\vpos in {1/93,2/104,3/115}{                                                      % they light up on step 6 (click 7)
      \node[tnode=vision,alt={<7->{line width=1.8pt,fill=vision!30}{}}] (v\vnum) at (\vpos,15.5) {vision};
      \draw[twig,line width=1.6pt] (104,9) -- (v\vnum);}
    \foreach \gnum/\gpos/\gvis in {1/77/1,2/86/1,3/95/2,4/104/2,5/113/2,6/122/3,7/131/3}{
      \node[tnode=goal,minimum width=7mm] (G\gnum) at (\gpos,24.5) {G\gnum};\draw[twig] (v\gvis) -- (G\gnum);}
    % ---------- the new growth, upward from the tip of G4 ----------
    \uncover<1->{\node[tnode=goal,alt={<1>{dashed}{}}] (bu) at (104,32) {goal bundle};}                % 0 the bundle (dashed until step 1 takes it up)
    \uncover<2->{\draw[shoot] (G4) -- (bu);                                                          % 1 director-goals: the subgoals = goal leaves
      \node[tnode=goal] (la) at (85,39.5) {goal};\draw[twig] (bu) -- (la);
      \node[tnode=goal] (lb) at (104,39.5) {goal};\draw[shoot] (bu) -- (lb);
      \node[tnode=goal] (lc) at (123,39.5) {goal};\draw[twig] (bu) -- (lc);}
    \uncover<3->{\node[tnode=hyp] (hy) at (104,46.5) {hypothesis};\draw[shoot] (lb) -- (hy);          % 2 director-science: hypotheses, then experiments
      \node[tnode=hyp,alt={<9>{opacity=0.3}{}}] (hz) at (79,46.5) {hypothesis};\draw[twig,alt={<9>{opacity=0.3}{}}] (la) -- (hz);
      \node[tnode=exp] (ex) at (104,53) {experiment};\draw[shoot] (hy) -- (ex);}
    \uncover<4->{\node[tnode=ink2] (mv) at (104,59.5) {mvp};\draw[shoot] (ex) -- (mv);                  % 3 director-general: mvp and build
      \node[tnode=ink2] (bn) at (104,66) {build};\draw[shoot] (mv) -- (bn);}
    \uncover<5->{\draw[ink,line width=1.2pt] (113,66) -- (113.9,65) -- (115.6,67.3);}                  % 4 director-review: reviewed
    \uncover<6->{\draw[ink,line width=1.2pt] (117.5,66) -- (118.4,65) -- (120.1,67.3);}                % 5 SM: checked again
    \uncover<7->{\draw[vision,line width=1.2pt] (122,66) -- (122.9,65) -- (124.6,67.3);}               % 6 council: checked against the visions
    \uncover<8->{\node[tnode=ink2] (ou) at (104,73) {outcome};\draw[shoot] (bn) -- (ou);}               % 7 Prime: landed; the shoot thickens (style shoot)
    \uncover<9->{\draw[serious,line width=1.6pt] (80.5,42.1) -- (83.5,43.9);                           % 8 the clipped branch regrows beside its stub
      \node[tnode=hyp,dashed] (hr) at (91,46.5) {hypothesis};\draw[twig,dashed,draw=goal] (la) -- (hr);}
  \end{tikzpicture}
  \note{V5 FLOW OF WORK (owner 11-10). Click k+1 = step k, nine clicks: 0 human + Prime, the goal bundle · 1 director-goals · 2 director-science · 3 director-general · 4 director-review, back to SM · 5 SM · 6 council, the visions light up · 7 Prime, it lands · 8 the send-back, with the return icon on every later role. The acting seat gets the thick border; the arrow is the hand-off; the tree gains that step's nodes.}
  \note{The workflow, owner 11-10, verbatim: The workflow should be Director goals splits the goal into subgoals, director science does the hypotheses and experiments, and director-general does the MVP and build nodes, and director-review reviews it and hands it back to SM who checks it again, then hands to the council who check it against their visions, and finally hand it off to the Prime. Each step can send it back for more work to any relevant director via SM as needed. (SM = sanctuary-master.)}
  \note{[empty slots, steps 0 to 8: the spoken line for each click is the owner's to write; the eleven v4 draft lines described the old flow and are removed.]}
\end{frame}

% ===== S8 what the project produced (0:45): overlay-built charts =====
\begin{frame}{The results so far} % OWNER c:pending-tap
  \begin{columns}[T]
  \column{0.58\textwidth}
    {\small How well could I get AI to reliably work on my project for days or weeks on end.}\\[3pt] % OWNER c:pending-tap
    \input{charts/s8-funnel.tex} % F1, owner-approved 11-10 (stats-graph.md, 2026-11-10); clicks 1-5
  \column{0.42\textwidth}
    \uncover<6->{{\small\bfseries What it takes to run it today:}\\[2pt] % OWNER c:pending-tap
    % F4 (owner 11-10): engine size, honest split (trace 11-09, town:core ## Fuel, meme-master block; static, upper bound). Page = ~50 lines, illustrative.
    \begin{tikzpicture}[x=0.5mm,y=1mm,font=\tiny]% bar lengths in thousands of lines (TeX caps a number near 16k)
      \foreach \y/\n/\lab/\pg/\c in {15/1.2/{shell engine, in the graph}/{$\approx$24 pages}/goal,10/84.5/{python it imports (upper bound)}/{$\approx$1,700 pages}/hyp,5/20.7/{python reached by name only}/{$\approx$400 pages}/hyp!50,0/15.9/{python nothing reaches (retire first)}/{$\approx$300 pages}/edge}{
        \fill[\c](0,\y)rectangle(\n,\y+3);
        \node[anchor=west,text=ink] at (\n+0.8,\y+1.5) {\lab~·~\pg};}
    \end{tikzpicture}\\[1pt]{\tiny\color{ink2}lines of code; book pages at $\sim$50 lines/page, illustrative}\\[4pt]}

    \uncover<7->{{\small\bfseries Statistically-significant data that many `dumber' agents matched or exceeded one `smarter' one}\\[3pt]} % OWNER c:pending-tap (the next step)
    \uncover<8->{\vclip{mn_triangle2}{C3t2 · manim · speed · coverage · cost · reprise of C3t}}
    \uncover<9->{\tmbox{lands/day chart}\\[3pt]\tmbox{benchmark}\\[3pt]
    {\footnotesize\color{ink2}METR 2025: predicted $-24\%$, measured $+19\%$.}}
  \end{columns}
  \note{OWNER (c:pending-tap), spoken on the next step: My vision of `success' is showing how the system allows many agents who may be less intelligent can effectively work together to match or outperform a significantly smarter model in any combination of speed, coverage, and cost. [visual: the S4 triangle again, re-labelled speed / coverage / cost: C3t2] \\
  OWNER (c:pending-tap), spoken on ``What it takes to run it today'': this is the engine as it is today, still in its prototype stage. The collaboration engine is using itself to create and upgrade the collaboration engine. [visual: C8 self-growing loop, storyboard-v5] \\
  OWNER (c:pending-tap), spoken: I like to say that my senior project is testing how can I get AI to do most of my senior project as autonomously as possible? It kinda makes sense, but kinda doesn't. I think the same is true when it comes to evaluating AI - it makes sense but it doesn't. We're really evaluating our ability to evaluate AI. It's really confusing in a wonderful, layered sort of way. \\
  Slots (test line now filled): [the correction: "104k lines" was wrong; ~1.2k lines of shell in graph nodes run the town, ~100k lines of older Python are being retired, in your words] · [measured-vs-predicted point, or skip] · [next step]. \\
  Cites: Becker et al. METR 2025, 16 devs, 246 tasks. Anthropic 2025: multi-agent about 15x chat tokens. Gartner 2025 PREDICTS >40\% of agentic projects canceled by end-2027 (news report).}
  \note{cleaned up rough draft written by AI: [empty slot, the title] What it produced, and why that is not proof yet}
  \note{cleaned up rough draft written by AI: [empty slot, what you set out to test] I set out to test whether a written graph of goals and results lets many agents work together better than one agent alone. I do not have that answer yet. What I have is a record of the attempts.}
  \note{cleaned up rough draft written by AI: [empty slot, the attempts] About 6,100 nodes. 2,393 experiments, 2,095 of them with a decided result. Roughly 15\% of those lean or land negative, and they are logged anyway. These numbers count how much the system did, not whether it helped. [figures: stats-graph.md, measured 11-10 by a file-count parse, not by the project's own tool]}
  \note{cleaned up rough draft written by AI: [empty slot, measured against predicted] In one 2025 study of 16 experienced developers, people predicted AI tools would make them 24\% faster. Measured, they were 19\% slower. Believing a tool helps is not the same as measuring it. [small sample, early-2025 tools, experts on their own code: say so]}
  \note{cleaned up rough draft written by AI: [empty slot, the next step] The next step is to name the test before running it: one agent against many, on the same task, with the passing line written down first.}
  \note{AI note: the slot for the correction (the engine's line counts) is left to you. Its figures are not in stats-graph.md, so no draft is offered.}
  \note{AI fact flags (RESOLVED 11-10 by meme-master: the old tiles are replaced by the funnel, stats-graph.md numbers) was: the tiles show 5,842 live nodes, about 25,400 commits and 426 reviewed lands, dated 11-07. stats-graph.md, measured 11-10, has 5,885 live nodes, 25,666 commits since 30 April, and 309 commits marked as a land, a naming habit that only began on 10-26; it counts 35 of them on 11-07 where the tile says 22. Reconcile before showing. Commit counts include merge and bot commits: never present them as human work.}
\end{frame}
% ----- S8b results bar (owner-approved 11-10) -----
\begin{frame}{The results so far} % OWNER c:pending-tap
  \centering\vspace{4mm}
  \input{charts/s8-results.tex} % F2: proved / leaning proved / leaning disproved / disproved, n = 2,095
  \note{Clicks 1-4: one bar each. 322 of 2,095 decided experiments are negative and logged anyway: the ``attempts'' (owner 11-10). The system's own six success metrics read UNMEASURED (stats-graph.md): keep them off screen; a honest beat if you want it.}
\end{frame}

% ===== S9 reveal + the question (0:45) =====
\begin{frame}{About that presentation} % OWNER c:pending-tap
  \vclip{hf_reveal}{C6 · HyperFrames · 10 s · real node ids}
  \note{OWNER (c:pending-tap): little speaking here; the owner wings it while the clip clicks through: the bigger goals, then the nested subgoals, then the research, skills and drafts the agents made (C6 v6 beats). \\
  Slots: [OWNER WRITES: who did what: your words vs agents' drafting, sourcing, measuring] · [the correction the graph caught: fuel:s4-retire-the-python-engine (retired; its THOUGHT holds the near miss)]. Q: proof, not a trick: how do you say "this talk is itself a node chain"? Decide: show the c: chunk ids or keep them elided.}
  \note{cleaned up rough draft written by AI: [empty slot, the title] This talk is a branch on that tree}
  \note{cleaned up rough draft written by AI: [empty slot, who did what] The words you heard were mine. Agents drafted the visuals, found the sources and counted the numbers, and an AI pass suggested cleaner wording that I accepted or rejected line by line.}
  \note{AI fact flag (not a rewording): if you adopt any AI rewording from these notes, ``every line is mine'' stops being exact. The draft above says it honestly; change it to match what you actually keep.}
\end{frame}
\begin{frame}{About that presentation\hfill{\small\color{ink2}fallback}}\steps{hf_reveal}\end{frame}
\begin{frame}[plain]
  \vspace{0.3cm}\vclip{hf_bookend}{C7 · HyperFrames · 6 s · the S1 bar returns}
  \centering{\usebeamerfont{title}How do we measure success?}   % OWNER (board, v1 slide 8); owner may reword
  \note{Slot: [OWNER WRITES: the question to the room, if not this one]. The bar from S1 comes back: the tick becomes ?, goal y becomes goal:g5.4.3, the badge reads verdict: pending.}
  \note{cleaned up rough draft written by AI: [empty slot, the question to the room, if not the one on screen] So: what would you accept as proof?}
  \note{AI note: the closing clip C7 still holds a blank for the threshold you would accept (storyboard-v3). That is a decision only you can make, so no draft is offered.}
\end{frame}
\begin{frame}[plain]\steps{hf_bookend}\end{frame}

% ===== references (cited on slides; V = verified on the primary page, S = secondary; tags from research-b) =====
\begin{frame}[allowframebreaks]{References}
  \tiny
  \begin{itemize}
    \item Liu, Lin, Hewitt, Paranjape, Bevilacqua, Petroni, Liang. Lost in the Middle. TACL 2023. \url{https://arxiv.org/abs/2307.03172} (V)
    \item Hong, Troynikov, Huber (Chroma). Context Rot. Jul 2025. \url{https://www.trychroma.com/research/context-rot} (V, vendor report)
    \item Brooks. The Mythical Man-Month. Addison-Wesley 1975/1995. (law wording V; pairwise count is arithmetic)
    \item Conway. How Do Committees Invent? Datamation, Apr 1968. (existence V; wording unverified)
    \item Cemri et al. Why Do Multi-Agent LLM Systems Fail? 2025. \url{https://arxiv.org/abs/2503.13657} (V; category shares summed from per-mode \%)
    \item Sinha, Arun, Goel, Staab, Geiping. The Illusion of Diminishing Returns. ICLR 2026. \url{https://arxiv.org/abs/2509.09677} (V, qualitative)
    \item Kwa et al. (METR). Measuring AI Ability to Complete Long Software Tasks. 2025. \url{https://arxiv.org/abs/2503.14499} (V)
    \item Qu, Zhang, Zhang, Deng, Li, Zhang, Liu. Overeager Coding Agents. May 2026. \url{https://arxiv.org/abs/2605.18583} (V, abstract)
    \item Anthropic. Building effective agents. Dec 2024. \url{https://www.anthropic.com/engineering/building-effective-agents} (V)
    \item Brown et al. Large Language Monkeys. 2024. \url{https://arxiv.org/abs/2407.21787} (V)
    \item Ron, Baudry, Monperrus. N-Version Programming with Coding Agents. Jun 2026. \url{https://arxiv.org/abs/2606.20158} (V, abstract)
    \item Knight, Leveson. An experimental evaluation of the assumption of independence in multiversion programming. IEEE TSE 1986. (V via abstracts)
    \item Yan (Cognition). Don't Build Multi-Agents. Jun 2025. \url{https://cognition.com/blog/dont-build-multi-agents} (V)
    \item Hong et al. MetaGPT. ICLR 2024. \url{https://arxiv.org/abs/2308.00352} (V)
    \item Becker, Rush, Barnes, Rein (METR). Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. 2025. \url{https://arxiv.org/abs/2507.09089} (V)
    \item Anthropic. How we built our multi-agent research system. Jun 2025. \url{https://www.anthropic.com/engineering/multi-agent-research-system} (V)
    \item Gartner press release, 25 Jun 2025, via The Star. (S: a prediction, not a measurement)
    \item Freeman. The Tyranny of Structurelessness. The Second Wave 2(1), 1972. \url{https://www.crmvet.org/comm/freemant.htm} (B)
    \item Davis, Lawrence. Problems of Matrix Organizations. Harvard Business Review 56(3):131--142, 1978. (B)
    \item Mintzberg. Structure in 5's: A Synthesis of the Research on Organization Design. Management Science 26(3):322--341, 1980. (B)
    \item Schwaber, Sutherland. The Scrum Guide. 2020. (U: not checked in this pass)
    \item Skelton, Pais. Team Topologies. IT Revolution Press, 2019. (B; year and publisher from memory)
    \item US Army. ADP 6-0, Mission Command. 2012. (B)
    \item Ohno. Toyota Production System: Beyond Large-Scale Production. Productivity Press, 1978/1988. (U: not checked in this pass)
    \item Doty, Glick, Huber. Fit, Equifinality, and Organizational Effectiveness. Academy of Management Journal 36(6):1196--1250, 1993. (B, abstract)
    \item Pedagogy behind the deck: Brame 2016, CBE-LSE, \url{https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380}; Tversky, Morrison, Betrancourt 2002.
  \end{itemize}
\end{frame}
\end{document}

````

## charts/s8-funnel.tex
````latex
% DRAFT chart F1 (owner-approved 11-10): the attempts funnel. Data: stats-graph.md (read-only counts, 2026-11-10).
% Labels are node-type names + counts only (no prose). \input inside a frame; uses the deck palette.
\begin{tikzpicture}[x=1mm,y=1mm,font=\small]
  \foreach \i/\lab/\n/\c in {0/goals/794/goal,1/ideas/159/idea,2/hypotheses/1529/hyp,3/experiments/2393/exp,4/results/2095/verdict}{
    \pgfmathsetmacro{\w}{\n/2393*70}
    \uncover<\the\numexpr\i+1\relax->{
      \fill[\c] (0,-\i*9) rectangle (\w,-\i*9-6);
      \node[anchor=east,text=ink] at (-2,-\i*9-3) {\lab};
      \node[anchor=west,text=ink2] at (\w+2,-\i*9-3) {\n};}}
  \node[anchor=west,font=\tiny,text=ink2] at (0,-48) {node counts, 2026-11-10 · results = experiments with a logged verdict};
\end{tikzpicture}

````

## charts/s8-results.tex
````latex
% DRAFT chart F2 (owner-approved 11-10): experiment results, n = 2,095 decided. Data: stats-graph.md.
\begin{tikzpicture}[x=1mm,y=0.045mm,font=\small]
  \foreach \i/\lab/\n/\c in {0/proved/1044/exp,1/leaning proved/729/exp!55,2/leaning disproved/240/verdict!55,3/disproved/82/verdict}{
    \uncover<\the\numexpr\i+1\relax->{
      \fill[\c] (\i*24,0) rectangle (\i*24+16,\n);
      \node[above,text=ink] at (\i*24+8,\n) {\n};
      \node[below,text=ink,align=center,text width=22mm] at (\i*24+8,0) {\lab};}}
  \draw[edge] (-3,0) -- (95,0);
  \node[anchor=west,font=\tiny,text=ink2] at (0,-250) {2,095 decided experiments, 2026-11-10 · 322 negative, logged anyway};
\end{tikzpicture}

````

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-10: the copy the council's full pass reads (alive's A1, aio's TERM, sp's ADD A/C). One course name and one faculty role elided; nothing else changed; the guard compared the owner lines after exactly the listed removals (equal). Storyboards and animation sources stay private for now; the clip rows the deck names are summarized in its own \note lines.
v2, same day: sp's RETURN 10:38:47Z taken: head fields moved above the first '## ' heading, the count in the leaf's control form; source lines 127 and 410 were agent paraphrases of owner asides wrongly labelled "OWNER's aside", relabelled in the private source and here ("Agent paraphrase of an owner aside (c:...), not verbatim"), so no owner line carries a removal; source sha256 changed with that relabel.
<!-- THOUGHT:END -->
