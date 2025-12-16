current_cv = r"""
\documentclass[11pt,a4paper]{article}

% --- encoding & language ---
\usepackage[T2A]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{hyphenat}

% --- layout & tools ---
\usepackage{geometry}
\geometry{margin=1.5cm}
\usepackage{paracol}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{microtype}

% --- colors & headings ---
\definecolor{headerbg}{gray}{0.92}
\definecolor{dark}{gray}{0.05}

\titleformat{\section}{\large\bfseries\color{dark}\centering}{}{0pt}{}
\titleformat{\subsection}{\normalsize\bfseries\color{dark}\raggedright}{}{0pt}{}

\setlist[itemize]{leftmargin=*, nosep, topsep=2pt, partopsep=0pt, parsep=0pt, itemsep=2pt}

\setlength{\columnsep}{12pt}
\setlength{\columnseprule}{0.3pt}
\columnratio{0.32,0.68}

\begin{document}

\pagestyle{empty}

% -------- Header --------
\noindent
\colorbox{headerbg}{%
  \parbox{\dimexpr\linewidth-2\fboxsep\relax}{%
    \centering\vspace{6pt}
    {\Huge\bfseries Uladzislau Kakhniuk}\\[1pt]
    {\large Fullstack Developer}\\[3pt]
  }%
}
\vspace{4pt}

\noindent\centering
\href{mailto:vladislavkohnuk2001@gmail.com}{vladislavkohnuk2001@gmail.com} \textbar{} +48 796 954 606\\Warsaw, Poland 

\vspace{6pt}

% -------- two columns --------
\begin{paracol}{2}

% -- left column --
\switchcolumn[0]

\section*{EDUCATION}
\begin{flushleft}
\textbf{Applied Computer Science}\\
Warsaw University of Technology\\
Part-Time Studies \\
2024--Present

\vspace{3pt}
\textbf{Automation of Technological Processes}\\
Belarusian National Technical University\\
2018--2020
\end{flushleft}

\vspace{5pt}\noindent\rule{\linewidth}{0.5pt}\vspace{5pt}

\section*{SKILLS}
\begin{flushleft}
\begin{itemize}
  \item Python (FastAPI), JavaScript / TypeScript (React, Redux, MUI)
  \item Microfrontend architecture, Module Federation
  \item Azure App Service, Azure AI Studio
  \item SQL / PostgreSQL, Docker, Git
  \item Prompt Engineering, GenAI Integrations (OpenAI, Claude, Gemini)
  \item Automation scripting, Testing (Selenium), CI/CD
\end{itemize}
\end{flushleft}

\vspace{5pt}\noindent\rule{\linewidth}{0.5pt}\vspace{5pt}

\section*{LANGUAGES}
\begin{flushleft}
\begin{itemize}
  \item English (C1)
  \item Polish (C2)
  \item Belarusian (Native)
  \item Russian (Native)
\end{itemize}
\end{flushleft}

% -- right column --
\switchcolumn

\section*{PROFILE}
\begin{flushleft}
\sloppy
Fullstack developer with strong focus on AI-driven solutions and modern web technologies.
Experienced in building scalable applications with Python/FastAPI and TypeScript/React,
and integrating LLM-based automation (OpenAI, Claude, Gemini) to accelerate workflows.
Familiar with deploying and maintaining cloud-based applications using Azure services.
Passionate about learning, experimenting with GenAI tools, and writing clean, efficient code.
\end{flushleft}

\section*{EXPERIENCE}
\begin{flushleft}
\subsection*{10Clouds\hfill September 2024 -- November 2025 (1 Year)}
\textit{Fullstack Developer}
\begin{itemize}
  \item Developed and maintained web applications using Python/FastAPI and TypeScript/React.  
  \item Implemented new frontend modules using React, Redux Toolkit.
  \item Developed modular frontend components using Module Federation for scalable web applications.
  \item Integrated external APIs and GenAI features (OpenAI, Claude, Gemini) for client solutions.  
  \item Deployed and tested apps using Azure and Docker containers.  
  \item Improved frontend responsiveness and reduced API latency by optimizing backend endpoints.  
\end{itemize}

\vspace{8pt}

\subsection*{Lionbridge \hfill May 2022 -- September 2024 (3 Years)}
\textit{Test Analyst}
\begin{itemize}
  \item Designed and documented detailed test cases and tasks, ensuring comprehensive coverage.  
  \item Coordinated testing efforts and monitored progress to ensure efficient QA execution.  
  \item Collaborated with development team to clarify requirements, report bugs, and support defect resolution.  
  \item Participated in planning and prioritization of QA activities to align testing with milestones.  
  \item Contributed to process improvements by identifying inefficiencies and proposing workflow optimizations.
\end{itemize}
\end{flushleft}

\end{paracol}

% --- GDPR note ---
\vfill
\begin{minipage}{\linewidth}
{\small\color{gray}
I agree to the processing of personal data provided in this document for realising the recruitment process pursuant to the Personal Data Protection Act of 10 May 2018 (Journal of Laws 2018, item 1000) and in agreement with Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation).
}
\end{minipage}

\end{document}
"""
