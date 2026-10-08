# Frame Patterns

Paste-ready LaTeX for the snippets in `latex_snippets.code-snippets`, expanded with
literal placeholder names in place of the editor's `${1:...}` tab stops. Substitute
every placeholder textually before use. `IMAGE.png` marks a filename slot — replace
each occurrence with the actual image for that slot, even where the same name
appears more than once in one entry.

## sourcepage — one approved teaching slide with our footer

Use only for an individually approved slide from a foreign teaching presentation.
Record the source handle and physical page in `PLAN.md` and the extracted PNG in
`PROVENANCE.json`. Whole presentations and book pages remain forbidden.

This ordinary untitled frame keeps the standard author, course title and frame number.
Do not add `plain`, a title, a background reset, or `\includepdf`. The height is bounded
to leave room above the footer; inspect the compiled page for each asset.

```latex
\begin{frame}[c]
    \centering
    \includegraphics[width=\textwidth,height=0.8\paperheight,keepaspectratio]{IMAGE.png}
\end{frame}
```

Substitute: `IMAGE.png`.

## figc — single figure with a numbered caption

Use for one image that needs a caption and a label.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{figure}[H]
        \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
        \caption{CAPTION TEXT}
        \label{fig:IMAGE.png}
    \end{figure}
\end{frame}
```

Substitute: `FRAME TITLE`, `IMAGE.png`, `CAPTION TEXT`.

## figclink — figure that is itself a hyperlink

Use when the whole image should open a URL (e.g. a live demo) when clicked.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{figure}[H]
        \href{LINK_URL}{
            \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}}
        \label{fig:IMAGE.png}
    \end{figure}
\end{frame}
```

Substitute: `FRAME TITLE`, `LINK_URL`, `IMAGE.png`.

## subfi2 — two side-by-side subfigures (49 / 49) under one caption

Use to compare two images of equal size sharing one main caption.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{figure}[H]
        \begin{subfigure}[t]{0.49\textwidth}
            \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION ONE}
            \label{fig:LABEL_ONE}
        \end{subfigure}
        \begin{subfigure}[t]{0.49\textwidth}
            \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION TWO}
            \label{fig:LABEL_TWO}
        \end{subfigure}

        \caption{CAPTION MAIN}
        \label{fig:LABEL_MAIN}
    \end{figure}
\end{frame}
```

Substitute: `FRAME TITLE`, `IMAGE.png` (once per image), `CAPTION ONE`, `LABEL_ONE`, `CAPTION TWO`, `LABEL_TWO`, `CAPTION MAIN`, `LABEL_MAIN`.

## subfi3 — three side-by-side subfigures (32 / 32 / 32) under one caption

Use to compare three images of equal size sharing one main caption.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{figure}[H]
        \begin{subfigure}[t]{0.32\textwidth}
            \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION ONE}
            \label{fig:LABEL_ONE}
        \end{subfigure}
        \begin{subfigure}[t]{0.32\textwidth}
            \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION TWO}
            \label{fig:LABEL_TWO}
        \end{subfigure}
        \begin{subfigure}[t]{0.32\textwidth}
            \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION THREE}
            \label{fig:LABEL_THREE}
        \end{subfigure}

        \caption{CAPTION MAIN}
        \label{fig:LABEL_MAIN}
    \end{figure}
\end{frame}
```

Substitute: `FRAME TITLE`, `IMAGE.png` (once per image), `CAPTION ONE`, `LABEL_ONE`, `CAPTION TWO`, `LABEL_TWO`, `CAPTION THREE`, `LABEL_THREE`, `CAPTION MAIN`, `LABEL_MAIN`.

## subfi4 — four subfigures in a 2x2 grid (49 / 49, 49 / 49) under one caption

Use to compare four images of equal size sharing one main caption, two per row.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{figure}[H]
        \begin{subfigure}[t]{0.49\textwidth}
            \centering\includegraphics[height=3cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION ONE}
            \label{fig:LABEL_ONE}
        \end{subfigure}
        \begin{subfigure}[t]{0.49\textwidth}
            \centering\includegraphics[height=3cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION TWO}
            \label{fig:LABEL_TWO}
        \end{subfigure}

        \begin{subfigure}[t]{0.49\textwidth}
            \centering\includegraphics[height=3cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION THREE}
            \label{fig:LABEL_THREE}
        \end{subfigure}
        \begin{subfigure}[t]{0.49\textwidth}
            \centering\includegraphics[height=3cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \caption{CAPTION FOUR}
            \label{fig:LABEL_FOUR}
        \end{subfigure}

        \caption{CAPTION MAIN}
        \label{fig:LABEL_MAIN}
    \end{figure}
\end{frame}
```

Substitute: `FRAME TITLE`, `IMAGE.png` (once per image), `CAPTION ONE`, `LABEL_ONE`, `CAPTION TWO`, `LABEL_TWO`, `CAPTION THREE`, `LABEL_THREE`, `CAPTION FOUR`, `LABEL_FOUR`, `CAPTION MAIN`, `LABEL_MAIN`.

The `height=3cm` above is tight: with four real images and four captions this frame overfills its
vbox by roughly 49 pt. The compile still succeeds and the slide still renders, but the bottom caption
sits low. If the QA gate or the PDF shows it crowded, drop the height to `2.4cm` rather than deleting
a caption.

## rsidecap — figure left, caption text right (58 / 40)

Use when a figure carries two to five lines of explanation that must sit beside it.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{minipage}[t]{0.58\textwidth}
        \includegraphics[width=\linewidth]{IMAGE.png}
    \end{minipage}
    \hfill
    \begin{minipage}[t]{0.40\textwidth}
        \vspace{0pt}
        CAPTION TEXT
    \end{minipage}
\end{frame}
```

Substitute: `FRAME TITLE`, `IMAGE.png`, `CAPTION TEXT`.

## lsidecap — caption text left, figure right (40 / 58)

Use when the explanation should be read before the figure it describes.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{minipage}[t]{0.40\textwidth}
        \vspace{0pt}
        CAPTION TEXT
    \end{minipage}
    \hfill
    \begin{minipage}[t]{0.58\textwidth}
        \includegraphics[width=\linewidth]{IMAGE.png}
    \end{minipage}
\end{frame}
```

Substitute: `FRAME TITLE`, `CAPTION TEXT`, `IMAGE.png`.

## nfr — bare frame with a subtitle

Use as the starting point for any ordinary text frame.

```latex
\begin{frame}[t]{FRAME TITLE}
\framesubtitle{FRAME SUBTITLE}
    BODY CONTENT
\end{frame}
```

Substitute: `FRAME TITLE`, `FRAME SUBTITLE`, `BODY CONTENT`.

## ncols — two-column layout (49 / 49)

Use to place two independent pieces of content side by side within one frame.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{columns}[T,onlytextwidth]
        \begin{column}{0.49\textwidth}
            LEFT CONTENT
        \end{column}
        \begin{column}{0.49\textwidth}
            RIGHT CONTENT
        \end{column}
    \end{columns}
\end{frame}
```

Substitute: `FRAME TITLE`, `LEFT CONTENT`, `RIGHT CONTENT`.

## blk — highlighted block

Use to visually set off a definition, theorem, or key takeaway.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{block}{BLOCK TITLE}
        BLOCK CONTENT
    \end{block}
\end{frame}
```

Substitute: `FRAME TITLE`, `BLOCK TITLE`, `BLOCK CONTENT`.

## m33 — 3x3 matrix

Use inside display math for a 3x3 matrix such as a rotation matrix.

```latex
\begin{frame}[t]{FRAME TITLE}
    \[
    \begin{bmatrix}
        A11 & A12 & A13 \\
        A21 & A22 & A23 \\
        A31 & A32 & A33
    \end{bmatrix}
    \]
\end{frame}
```

Substitute: `FRAME TITLE`, `A11`\ldots`A33` (nine matrix entries).

## m44 — 4x4 matrix

Use inside display math for a 4x4 matrix such as a homogeneous transform.

```latex
\begin{frame}[t]{FRAME TITLE}
    \[
    \begin{bmatrix}
        A11 & A12 & A13 & A14 \\
        A21 & A22 & A23 & A24 \\
        A31 & A32 & A33 & A34 \\
        A41 & A42 & A43 & A44
    \end{bmatrix}
    \]
\end{frame}
```

Substitute: `FRAME TITLE`, `A11`\ldots`A44` (sixteen matrix entries).

## v3 — 3-entry column vector

Use inside display math for a 3D vector.

```latex
\begin{frame}[t]{FRAME TITLE}
    \[
    \begin{bmatrix} V1 \\ V2 \\ V3 \end{bmatrix}
    \]
\end{frame}
```

Substitute: `FRAME TITLE`, `V1`, `V2`, `V3`.

## ucom — brace and comment under a formula

Use to label part of a formula with a short note underneath it.

```latex
\begin{frame}[t]{FRAME TITLE}
    \[
    \underbrace{FORMULA}_{TEXT}
    \]
\end{frame}
```

Substitute: `FRAME TITLE`, `FORMULA`, `TEXT`.

## utext — text annotation pointing up into a formula from below

Use to annotate a formula with an explanatory label placed underneath it.

```latex
\begin{frame}[t]{FRAME TITLE}
    \[
    \underset{\substack{\downarrow \\ \text{TEXT}}}{FORMULA}
    \]
\end{frame}
```

Substitute: `FRAME TITLE`, `TEXT`, `FORMULA`.

## otext — text annotation pointing down into a formula from above

Use to annotate a formula with an explanatory label placed above it.

```latex
\begin{frame}[t]{FRAME TITLE}
    \[
    \overset{\substack{\uparrow \\ \text{TEXT}}}{FORMULA}
    \]
\end{frame}
```

Substitute: `FRAME TITLE`, `TEXT`, `FORMULA`.

## hrf — inline hyperlink

Use for clickable text inline within a sentence.

```latex
\begin{frame}[t]{FRAME TITLE}
    \href{LINK_URL}{LINK TEXT}
\end{frame}
```

Substitute: `FRAME TITLE`, `LINK_URL`, `LINK TEXT`.

## ntaskframe — task frame with a click-to-reveal answer

Use for a problem whose answer is revealed on a second click.
Answer content is internal only; never use this answer overlay in a published homework.

```latex
\begin{frame}[t]{Task TASK NUMBER}
    \framesubtitle{}
    TASK BODY
    \uncover<2->{
        \alert{\Large Answer}
        ANSWER BODY
    }
\end{frame}
```

Substitute: `TASK NUMBER`, `TASK BODY`, `ANSWER BODY`.

## ntaskframefig — task frame with a question image and a revealed answer image

Use for a problem/answer pair that are both images, such as a diagram and its solved version.
Answer images are internal only; never use them in a published homework.

```latex
\begin{frame}[t]{Task TASK NUMBER}
    \framesubtitle{}
    \vspace{-0.5cm}
    \begin{figure}[H]
        \centering\includegraphics[height=3cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
        \label{fig:TASK_LABEL}
    \end{figure}
    \uncover<2->{
        \alert{\Large Answer}
        \begin{figure}[H]
            \centering\includegraphics[height=3cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
            \label{fig:ANSWER_LABEL}
        \end{figure}
    }
\end{frame}
```

Substitute: `TASK NUMBER`, `IMAGE.png` (once for the task image, once for the answer image), `TASK_LABEL`, `ANSWER_LABEL`.

## nonefigfr — frame subtitle plus one full-width figure

Use for a single supporting image alongside a frame subtitle, with no caption.

```latex
\begin{frame}[t]{FRAME TITLE}
\framesubtitle{FRAME SUBTITLE}
    \vspace{-0.6cm}
    \begin{figure}[H]
        \centering\includegraphics[height=6cm,width=1\textwidth,keepaspectratio]{IMAGE.png}
        \label{fig:IMAGE.png}
    \end{figure}
\end{frame}
```

Substitute: `FRAME TITLE`, `FRAME SUBTITLE`, `IMAGE.png`.

## multcols — multi-column itemized list

Use to spread a long itemized list across two (or more) columns.

```latex
\begin{frame}[t]{FRAME TITLE}
    \begin{multicols}{2}
        \begin{itemize}
            \item LIST ITEM
        \end{itemize}
    \end{multicols}
\end{frame}
```

Substitute: `FRAME TITLE`, `LIST ITEM`, and the column count `2`.

## todoin — inline TODO marker

Use to leave a visible reminder in the compiled slide while drafting.

```latex
\begin{frame}[t]{FRAME TITLE}
    \todo[inline]{TODO TEXT}
\end{frame}
```

Substitute: `FRAME TITLE`, `TODO TEXT`.
