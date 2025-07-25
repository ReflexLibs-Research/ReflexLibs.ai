<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="color-scheme" content="light dark">
    <title>ReflexLibs Timeline</title>
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet" />
 <style>
    /* basic page layout */
    body {
        margin: 0;
        display: flex;
        font-family: 'Poppins', sans-serif;
        height: 100vh;
    }

    .column {
        width: 50%;
        overflow-y: auto;
        padding: 1rem 2rem;
        box-sizing: border-box;
    }

    /* 1) remove markers from all lists by default */
    .column ul {
        list-style: none;
        margin: 0;
        padding-left: 0;
    }

    /* background variants */
    .white-bg {
        background: #fff;
        color: #000;
    }

    .black-bg {
        background: #000;
        color: #fff;
    }

    /* optional SVG header sizing */
    .svg-header img {
        max-width: 400px;
        width: 100%;
        height: auto;
        display: block;
        margin: 0 auto 1rem;
    }

    /* language box container */
    .lang-box {
        border-radius: 16px;
        padding: 1rem;
        width: 480px;
        margin: 0 auto 1rem;
    }
    .white-bg .lang-box {
        background: #f9f9f9;
        border: 1px solid #ddd;
    }
    .black-bg .lang-box {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* 2) re-enable bullets here and box them */
    .lang-box ul {
        list-style-type: disc;       /* show discs */
        list-style-position: inside; /* bullets inside padding */
        background: #f0f0f0;         /* fill */
        border: 1px solid #ccc;      /* outline */
        border-radius: 8px;          /* rounded corners */
        padding: 0.75rem 1rem;       /* space around items */
        margin: 0 0 1rem;            /* bottom gap */
    }
    .lang-box li {
        margin-bottom: 0.5rem;
    }

    /* icon row */
    .icon-container {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-bottom: 0.5rem;
    }
    .icon-container img {
        width: 48px;
        height: 48px;
    }

    /* timeline sections */
    .section {
        margin-bottom: 2rem;
    }
    .title {
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    /* 3) keep these lists bullet-free and flush */
    .section ul {
        list-style: none;
        margin: 0;
        padding-left: 0;
    }
    .section li {
        margin-bottom: 0.25rem;
    }
</style>
</head>

<body>
    <div id="left-container" class="column"></div>
    <div id="right-container" class="column"></div>

    <!-- SCRIPT AT BOTTOM SO #left-container/#right-container EXIST -->
    <script>
        const DotComOrAI = 'AI'; // or 'AI'

        const apiBase = 'https://devriskevolutionwebservice.azurewebsites.net/reflexLibs/';
        const logoBase = apiBase + 'ReflexLibsLogo/';
        const iconBase = 'https://devriskevolutionwebservice.azurewebsites.net/Icon/Generic/Get?Category=math&SubCategory=ProgLanguage&Size=64x64&Name=';

        const configs = {
            com: {
                apiUrl: apiBase + 'reflexlibs2018',
                langApi: apiBase + 'reflexlanguages2018',
                logoUrl: logoBase + 'com',
                icons: ['CPlusPlus', 'CSharp'],
                link: 'https://www.reflexlibs.com',
                bgClass: 'white-bg'
            },
            ai: {
                apiUrl: apiBase + 'reflexlibs2025',
                langApi: apiBase + 'reflexlanguages2025',
                logoUrl: logoBase + 'ai',
                icons: ['CPlusPlus', 'CSharp', 'Python', 'Rust', 'JavaScript'],
                link: 'https://www.reflexlibs.ai',
                bgClass: 'black-bg'
            }
        };

        const layoutMap = {
            DotCom: { left: configs.com, right: configs.ai },
            AI: { left: configs.ai, right: configs.com }
        };

        const layout = layoutMap[DotComOrAI];

        function renderColumn(containerId, cfg) {
            const c = document.getElementById(containerId);
            c.className = `column ${cfg.bgClass}`;

            const link = document.createElement('a');
            link.href = cfg.link;
            link.target = '_blank';

            const logo = document.createElement('img');
            logo.src = cfg.logoUrl;
            logo.alt = 'ReflexLibs Logo';
            link.appendChild(logo);
            c.appendChild(link);

            const box = document.createElement('div');
            box.className = 'lang-box';

            const iconsDiv = document.createElement('div');
            iconsDiv.className = 'icon-container';

            cfg.icons.forEach(name => {
                const img = document.createElement('img');
                img.src = iconBase + encodeURIComponent(name);
                img.alt = name;
                iconsDiv.appendChild(img);
            });

            box.appendChild(iconsDiv);

            const bulletsDiv = document.createElement('div');
            box.appendChild(bulletsDiv);
            c.appendChild(box);

            fetch(cfg.langApi, { headers: { 'Accept': 'application/json' }, cache: 'no-cache' })
                .then(r => r.ok ? r.json() : Promise.reject(r.status))
                .then(data => {
                    const list = Array.isArray(data.bullets) ? data.bullets
                        : Array.isArray(data.Bullets) ? data.Bullets
                            : [];

                    if (list.length) {
                        const ul = document.createElement('ul');
                        list.forEach(txt => {
                            const li = document.createElement('li');
                            li.textContent = txt;
                            ul.appendChild(li);
                        });
                        bulletsDiv.appendChild(ul);
                    }
                })
                .catch(e => console.error('Bullets error:', e));

            fetch(cfg.apiUrl, { headers: { 'Accept': 'application/json' }, cache: 'no-cache' })
                .then(r => r.ok ? r.json() : Promise.reject(r.status))
                .then(sections => {
                    sections.forEach(s => {
                        const sec = document.createElement('div');
                        sec.className = 'section';

                        const t = document.createElement('div');
                        t.className = 'title';
                        t.textContent = `${s.sectionID}. ${s.title}`;
                        sec.appendChild(t);

                        const ul = document.createElement('ul');
                        (s.items || []).forEach(item => {
                            const li = document.createElement('li');
                            li.textContent = item;
                            ul.appendChild(li);
                        });

                        sec.appendChild(ul);
                        c.appendChild(sec);
                    });
                })
                .catch(e => console.error('Sections error:', e));
        }

        renderColumn('left-container', layout.left);
        renderColumn('right-container', layout.right);
    </script>
</body>

</html>
