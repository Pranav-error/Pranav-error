<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1f6feb,100:58a6ff&height=200&section=header&text=Sai%20Pranav&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Software%20Engineer%20%7C%20Open-source%20C%20%7C%20AI%2FML&descAlignY=60&descSize=18" width="100%"/>

<a href="https://saipranav.me">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=640&lines=SDE+Intern+%40+Cepheid+(Danaher);50%2B+patches+merged+upstream+in+C;Hunting+memory+bugs+in+PostgreSQL+tooling;Building+tools+developers+actually+use" alt="Typing SVG" />
</a>

[![Portfolio](https://img.shields.io/badge/saipranav.me-000000?style=for-the-badge&logo=googlechrome&logoColor=white)](https://saipranav.me)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rsaipranav/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rajasaipranav0@gmail.com)

</div>

I'm a final-year CS student at REVA University (Bengaluru) and an SDE intern on the manufacturing-systems team at Cepheid (Danaher). Most of my spare time goes into open-source C: reading unfamiliar codebases, finding memory-safety and correctness bugs, and getting the fixes merged with a reproduction attached.

---

## Open source

Upstream work on C and Python projects — mostly memory-safety and correctness fixes, each with a reproduction and a regression test where the project supports one.

<div align="center">

<img src="https://img.shields.io/github/issues-search?query=author%3APranav-error%20is%3Apr%20is%3Amerged&label=PRs%20merged&color=8957e5&style=for-the-badge&logo=github" />
&nbsp;
<img src="https://img.shields.io/github/issues-search?query=author%3APranav-error%20is%3Apr%20is%3Aopen&label=PRs%20open&color=1f6feb&style=for-the-badge&logo=github" />
&nbsp;
<img src="https://img.shields.io/github/issues-search?query=author%3APranav-error%20is%3Aissue%20is%3Apublic&label=issues%20filed&color=238636&style=for-the-badge&logo=github" />

</div>

<!-- OSS:START -->

<div align="center">

| Project | Contribution | Status |
|:--|:--|:--|
| **[pgmoneta](https://github.com/pgmoneta/pgmoneta)** | Double frees, use-after-free, unchecked allocations, an off-by-one stack overflow, error-path null dereferences, and corner-case tests for the core string helpers | **22 merged** · 19 open |
| **[pgagroal](https://github.com/pgagroal/pgagroal)** | An unbounded `strcat` stack overflow in the CLI, unchecked reallocs, and silent truncation in the numeric append helpers — found by writing the corner-case tests | **15 merged** · 7 open |
| **[pgvictoria](https://github.com/pgvictoria/pgvictoria)** | Cross-ported allocation checks and string-helper fixes, with corner-case tests for the append family | **7 merged** · 9 open |
| **[pgexporter](https://github.com/pgexporter/pgexporter)** | Unchecked allocations in the YAML and network paths, plus a kqueue accept-drain fix ported from pgagroal | **13 merged** · 1 open |
| **[grass](https://github.com/OSGeo/grass)** | Null pointer dereference in the vector library, a null *function pointer* crash in `v.to.rast`, 64-bit cell counters, and unbounded environment growth in the runtime setup | **5 merged** · 5 open |
| **[website](https://github.com/kubernetes/website)** | Docs fixes, and a style guide section defining *deprecated* vs *no longer served* vs *removed* for APIs | **2 merged** · 2 open |
| **[jabref](https://github.com/JabRef/jabref)** | Repaired fetcher tests that broke when upstream metadata services changed their responses | **3 merged** |
| **[gnuradio](https://github.com/gnuradio/gnuradio)** | QA test for the real-time scheduling bindings, and float-tolerance fixes for two numeric tests that compared approximations for bit equality | **2 merged** · 1 open |
| **[hiring-agent](https://github.com/interviewstreet/hiring-agent)** | AI agent to evaluate and score resumes. | 2 open |
| **[Builder-Prod](https://github.com/Site-Analysis/Builder-Prod)** | Production ready clean product | 2 open |

</div>

<!-- OSS:END -->

---

## Writing

- **[Two stack overflows hiding in plain sight](https://dev.to/pranav-error/two-stack-overflows-hiding-in-plain-sight-1on2)** — a `strcat` into 512 bytes in pgagroal and a `"%.8f"` into 30 bytes in GRASS GIS: how I found them, proved them, and picked the fix each project would accept.

---

## Featured projects

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Pranav-error/claude-orchestrator">claude-orc</a></h3>
      <p>A control plane for Claude Code across multiple accounts and machines: git-backed memory sync, a skill registry, and token-usage reports parsed from local transcripts. Stdlib-only Python, 160+ tests in CI on 3.10–3.13, released to PyPI by CI.</p>
      <code>pip install claude-orc</code>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Pranav-error/evidence-verifier">Evidence Verifier</a></h3>
      <p>Is this invoice real? Checks whether a document's independent encodings agree — signed QR, text layer, line-item arithmetic, amount in words, PDF structure — instead of pixel forensics. Zero false positives across 9 independent corpora. Razorpay AI Buildathon.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Pranav-error/infrx-mortgage-pipeline">Mortgage document pipeline</a></h3>
      <p>Splits 100–2,000-page mortgage packages into 27 document types at 91% accuracy. A cost-aware cascade keeps most pages away from the LLM; Naive Bayes stitches tables split across pages. 2nd place, InfrX 2026.</p>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Pranav-error/OrbitClean-2.0">OrbitClean 2.0</a></h3>
      <p>Waste intelligence for Bengaluru: Sentinel-2 dump detection, XGBoost risk prediction over a 552-cell grid, and route optimisation, behind a FastAPI + Next.js dashboard. Top 5, AWI SpaceTech Hackathon.</p>
    </td>
  </tr>
</table>

All 40+ projects, grouped by area: **[saipranav.me](https://saipranav.me)** — or open the terminal there and type `ls projects`.

---

## Experience

- **SDE Intern, MES** — Cepheid India (Danaher) · Sep 2026 – present
- **Backend Developer (freelance)** — Contralyne, AI contract review · May – Sep 2026
- **Software Engineering Intern** — MyStartupWave · Dec 2025 – Aug 2026
- **Project Intern, Cybersecurity** — iSPIRT Foundation · Nov 2025 – Aug 2026
- **Research Intern, Explainable AI** — CSIR-4PI · Jul 2025 – Jan 2026

---

## Tools I use

<div align="center">

[![Skills](https://skillicons.dev/icons?i=c,cpp,python,java,ts,js,nodejs,react,nextjs,fastapi,postgres,mongodb,docker,aws,linux,git&theme=dark)](https://skillicons.dev)

</div>

---

## Contributions

<div align="center">

<img src="https://raw.githubusercontent.com/Pranav-error/Pranav-error/main/profile-3d-contrib/profile-night-rainbow.svg" width="100%" alt="3D contribution graph"/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Pranav-error/Pranav-error/output/github-snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Pranav-error/Pranav-error/output/github-snake.svg"/>
  <img alt="Contribution snake" src="https://raw.githubusercontent.com/Pranav-error/Pranav-error/output/github-snake.svg" width="100%"/>
</picture>

</div>

---

## 🏆 GitHub Trophies

<div align="center">

[![trophy](https://github-profile-trophy.vercel.app/?username=pranav-error&theme=tokyonight&no-frame=true&no-bg=true&margin-w=6&column=7)](https://github.com/ryo-ma/github-profile-trophy)

</div>

---

## 😂 Random Dev Joke

<div align="center">

![Jokes Card](https://readme-jokes.vercel.app/api?hideBorder&theme=tokyonight&qColor=%2358a6ff&aColor=%23c9d1d9)

</div>

---

## 💡 Dev Quote of the Day

<div align="center">

[![Readme Quotes](https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight)](https://github.com/piyushsuthar/github-readme-quotes)

</div>
