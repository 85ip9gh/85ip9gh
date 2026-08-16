<h1 align="center">Pesanth Janaseth</h1>

<p align="center">
  Software engineer · AI-assisted development · Halifax, Canada
</p>

<p align="center">
  Full-stack engineer with 2+ years of experience delivering financial applications,<br />
  cloud pipelines, and REST APIs, including AI-assisted development with proven productivity improvements.
</p>

<p align="center">
  <a href="https://pesanth.com"><img alt="Portfolio" src="https://img.shields.io/badge/Portfolio-pesanth.com-171717?style=flat-square&logo=googlechrome&logoColor=white" /></a>
  <a href="https://pesanth.com/resume/Pesanth_Resume.pdf"><img alt="Résumé" src="https://img.shields.io/badge/Résumé-PDF-525252?style=flat-square&logo=readthedocs&logoColor=white" /></a>
  <a href="https://www.linkedin.com/in/pesanth-janaseth-rangaswamy-anitha-75755b199/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Profile-525252?style=flat-square" /></a>
  <a href="mailto:contact@pesanth.com"><img alt="Email" src="https://img.shields.io/badge/Email-contact%40pesanth.com-525252?style=flat-square" /></a>
</p>

<p align="center">
  <sub>Open to software engineering roles in Canada.</sub>
</p>

## Selected projects.

Flagship full-stack systems, cloud backend services, and AI reliability tooling. Every project below has a technical overview covering its purpose, architecture, engineering decisions, verification evidence, and limitations.

### Sentinel

[![Sentinel live site](https://img.shields.io/badge/Live-sentinel.pesanth.com-171717?style=flat-square&logo=apachekafka&logoColor=white)](https://sentinel.pesanth.com)
[![Sentinel overview](https://img.shields.io/badge/Architecture-Technical_overview-525252?style=flat-square&logo=diagramsdotnet&logoColor=white)](https://pesanth.com/work/sentinel)
![Source private](https://img.shields.io/badge/Source-Private-6F6F6F?style=flat-square&logo=github&logoColor=white)

A streaming telemetry platform that collects readings from two self-hosted machines every ten seconds, moves them through Kafka, and archives them in day-partitioned HDFS storage that a public dashboard reads back. Collectors buffer to local disk when the broker is unreachable and replay in order once it returns, and stream offsets are committed only after each batch reaches storage.

### arXiv Daily Digest

[![arXiv Daily Digest live site](https://img.shields.io/badge/Live-papers.pesanth.com-171717?style=flat-square&logo=arxiv&logoColor=white)](https://papers.pesanth.com)
[![arXiv Daily Digest overview](https://img.shields.io/badge/Architecture-Technical_overview-525252?style=flat-square&logo=diagramsdotnet&logoColor=white)](https://pesanth.com/work/arxiv-daily-digest)
![Source private](https://img.shields.io/badge/Source-Private-6F6F6F?style=flat-square&logo=github&logoColor=white)

A scheduled pipeline that reads the day's new AI papers on arXiv, selects three, and summarizes each from the body of the paper rather than its abstract. Two automated checks stand between the model and the page: the quoted fragment must appear in the paper, and every figure written must appear in it too. A summary that fails either check is published marked unverified rather than presented as checked.

### Car Sale Application

[![Car Sale Application live site](https://img.shields.io/badge/Live-carsale.pesanth.com-171717?style=flat-square&logo=springboot&logoColor=white)](https://carsale.pesanth.com)
[![Car Sale Application repository](https://img.shields.io/badge/Source-Repository-525252?style=flat-square&logo=github&logoColor=white)](https://github.com/85ip9gh/car-sale-application)
[![Car Sale Application overview](https://img.shields.io/badge/Architecture-Technical_overview-525252?style=flat-square&logo=diagramsdotnet&logoColor=white)](https://pesanth.com/work/car-sale-application)

A React and Spring Boot peer-to-peer car marketplace with JWT authentication, role-based access, MySQL persistence, and Docker packaging. Live at [carsale.pesanth.com](https://carsale.pesanth.com), self-hosted on a Linux server behind an outbound-only Cloudflare Tunnel. Sign in as `demo` / `demo1234` to browse the market, list a vehicle, and buy from another seller.

### Cube Store

[![Cube Store live site](https://img.shields.io/badge/Live-cubestore.pesanth.com-171717?style=flat-square&logo=angular&logoColor=white)](https://cubestore.pesanth.com)
[![Cube Store repository](https://img.shields.io/badge/Source-Repository-525252?style=flat-square&logo=github&logoColor=white)](https://github.com/85ip9gh/cube-store-application)
[![Cube Store overview](https://img.shields.io/badge/Architecture-Technical_overview-525252?style=flat-square&logo=diagramsdotnet&logoColor=white)](https://pesanth.com/work/cube-store)

A full-stack Angular and Express commerce platform with MongoDB, Stripe Checkout, responsive product discovery, cart workflows, and Docker packaging. Live at [cubestore.pesanth.com](https://cubestore.pesanth.com), self-hosted behind the same tunnel. The public demo is deliberately read-only: browse, search, and filter all 66 products, with checkout disabled.

### Incident Triage Assistant

[![Incident Triage Assistant overview](https://img.shields.io/badge/Architecture-Technical_overview-525252?style=flat-square&logo=diagramsdotnet&logoColor=white)](https://pesanth.com/work/incident-triage-assistant)
![Source private](https://img.shields.io/badge/Source-Private-6F6F6F?style=flat-square&logo=github&logoColor=white)

A retrieval-augmented incident-triage workflow with a dependency-free BM25 index, structured Claude outputs, a CLI, a Streamlit interface, and an offline evaluation suite.

### WinGet App Installer

[![WinGet App Installer repository](https://img.shields.io/badge/Source-Repository-525252?style=flat-square&logo=github&logoColor=white)](https://github.com/85ip9gh/winget-app-installer)
[![WinGet App Installer release](https://img.shields.io/badge/Download-Latest_release-171717?style=flat-square&logo=github&logoColor=white)](https://github.com/85ip9gh/winget-app-installer/releases/latest)
[![WinGet App Installer overview](https://img.shields.io/badge/Architecture-Technical_overview-525252?style=flat-square&logo=diagramsdotnet&logoColor=white)](https://pesanth.com/work/winget-app-installer)

A Windows desktop utility for discovering, selecting, and bulk-installing WinGet packages through a guided interface, with automated release builds and downloadable binaries.

## Production work with measurable outcomes.

![Delivery pipelines](https://img.shields.io/badge/CI%2FCD_pipelines_delivered-39%2B-171717?style=flat-square)
![Production incidents](https://img.shields.io/badge/Production_incidents_resolved-50%2B-171717?style=flat-square)
![Dashboard components](https://img.shields.io/badge/Financial_dashboard_components-24%2B-171717?style=flat-square)

- Delivered 39+ Azure CI/CD pipelines using Ansible and Docker.
- Resolved 50+ production incidents through log analysis, diagnosis, and root-cause investigation.
- Built customer-facing financial dashboards across 24+ components.

## Capabilities.

**Core languages and application development**

![Java](https://img.shields.io/badge/Java-6F6F6F?style=flat-square&logo=openjdk&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-6F6F6F?style=flat-square&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-6F6F6F?style=flat-square&logo=javascript&logoColor=white)
![Python](https://img.shields.io/badge/Python-6F6F6F?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-6F6F6F?style=flat-square&logo=postgresql&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6F6F6F?style=flat-square&logo=springboot&logoColor=white)
![Angular](https://img.shields.io/badge/Angular-6F6F6F?style=flat-square&logo=angular&logoColor=white)
![React](https://img.shields.io/badge/React-6F6F6F?style=flat-square&logo=react&logoColor=white)
![Express](https://img.shields.io/badge/Express-6F6F6F?style=flat-square&logo=express&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-6F6F6F?style=flat-square&logo=mongodb&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-6F6F6F?style=flat-square&logo=mysql&logoColor=white)

**Cloud, delivery, and reliability**

![Docker](https://img.shields.io/badge/Docker-6F6F6F?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-6F6F6F?style=flat-square&logo=kubernetes&logoColor=white)
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-6F6F6F?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-6F6F6F?style=flat-square)
![Ansible](https://img.shields.io/badge/Ansible-6F6F6F?style=flat-square&logo=ansible&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-6F6F6F?style=flat-square&logo=githubactions&logoColor=white)
![Datadog](https://img.shields.io/badge/Datadog-6F6F6F?style=flat-square&logo=datadog&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-6F6F6F?style=flat-square&logo=apachekafka&logoColor=white)
![Hadoop HDFS](https://img.shields.io/badge/Hadoop_HDFS-6F6F6F?style=flat-square&logo=apachehadoop&logoColor=white)

## GitHub activity.

<p align="center">
  <img width="49%" src="./assets/github-stats.svg" alt="Pesanth's verified GitHub snapshot" />
  <img width="49%" src="./assets/top-languages.svg" alt="Languages used across Pesanth's public repositories" />
</p>

<sub>Verified through GitHub on 2026-07-23. Contribution totals use GitHub's twelve-month contribution calendar; language percentages use GitHub-reported bytes across owned public repositories.</sub>

## Explore the architecture.

Every featured project has a recruiter-friendly technical overview covering its purpose, use cases, top-down architecture, engineering decisions, verification evidence, and limitations.

[![Explore the portfolio](https://img.shields.io/badge/Explore_all_projects-pesanth.com-171717?style=flat-square&logo=googlechrome&logoColor=white)](https://pesanth.com/#work)
