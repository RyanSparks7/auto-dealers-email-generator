import json, os

city_data = json.load(open('city_dealers.json', encoding='utf-8'))
city_data_js = json.dumps(city_data, ensure_ascii=False, separators=(',',':'))

LENDERS_JS = """const LENDERS = [
  { name:"ACC Consumer Finance",           states:["AZ","AR","CA","CO","FL","GA","IN","KY","MD","NC","NJ","OH","OR","PA","TN","TX","VA"], segment:"Non-Prime",  fico:"525+" },
  { name:"Anchored Finance, LLC",          states:["AZ","CA","CT","FL","GA","KY","MA","MI","NJ","NC","ND","OK","OH","PA","SC","TX","UT","WI"], segment:"Non-Prime / Prime", fico:"560+" },
  { name:"Financial Partners FCU",         states:["IN"],                                       segment:"Prime",           fico:"580+" },
  { name:"First Bank of Ohio",             states:["KY","IN","MI","PA","WV"],                   segment:"Prime",           fico:"630+" },
  { name:"Old Point National Bank",        states:["FL","NC","SC","VA"],                        segment:"Prime",           fico:"625+" },
  { name:"Arrha Credit Union",             states:["CT","MA"],                                  segment:"Non-Prime / Prime", fico:"581+" },
  { name:"Clearpath Federal Credit Union", states:["CA"],                                       segment:"Prime",           fico:"630+" },
  { name:"EV Life",                        states:["CA","NC","MI"],                             segment:"Prime (EV Only)", fico:"680+" },
  { name:"First Consumer Financial",       states:["GA","LA","MS","TN"],                        segment:"Deep Subprime",   fico:"460+" },
  { name:"Greenwood Credit Union",         states:["CT","MA","ME","RI"],                        segment:"Prime",           fico:"600+" },
  { name:"Peoples Credit Union",           states:["CT","MA","RI","VT"],                        segment:"Non-Prime / Prime", fico:"581+" },
  { name:"LUSO Federal Credit Union",      states:["CT","MA"],                                  segment:"Prime",           fico:"630+" },
  { name:"First Flight FCU",               states:["NC","SC","VA"],                             segment:"Prime",           fico:"600+" },
  { name:"Glenview Finance",               states:["AL","FL","GA","IN","KY","NC","OH","SC","TN","VA","TX"], segment:"Sub-Prime", fico:"580+" },
  { name:"K.A.R.T Trust",                  states:["AZ","CA","CT","FL","GA","KY","MA","MI","NJ","NC","ND","OK","OH","PA","SC","TX","UT","WI"], segment:"Non-Prime / Prime", fico:"580+" },
  { name:"Gravity Lending",                states:["ALL"],                                      segment:"Non-Prime / Prime (Refi)", fico:"581+" },
];"""

STATE_NAMES_JS = """const STATE_NAMES = {AZ:"Arizona",AR:"Arkansas",CA:"California",CO:"Colorado",CT:"Connecticut",FL:"Florida",GA:"Georgia",ID:"Idaho",IL:"Illinois",IN:"Indiana",KY:"Kentucky",LA:"Louisiana",MA:"Massachusetts",MD:"Maryland",ME:"Maine",MI:"Michigan",MN:"Minnesota",MO:"Missouri",MS:"Mississippi",NC:"North Carolina",ND:"North Dakota",NJ:"New Jersey",NV:"Nevada",NY:"New York",OH:"Ohio",OK:"Oklahoma",OR:"Oregon",PA:"Pennsylvania",RI:"Rhode Island",SC:"South Carolina",SD:"South Dakota",TN:"Tennessee",TX:"Texas",UT:"Utah",VA:"Virginia",VT:"Vermont",WA:"Washington",WI:"Wisconsin",WV:"West Virginia"};"""

html_parts = []

html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auto Dealers Digital \u2014 Email Generator</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root {
    --teal:   #00C8B4;
    --teal-d: #00a899;
    --black:  #1a1a1a;
    --white:  #ffffff;
    --gray:   #f5f5f5;
    --mid:    #888888;
    --border: #e5e5e5;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family:'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--gray);
    min-height:100vh;
    display:flex; flex-direction:column;
    color: var(--black);
  }
  .page { display:none; flex:1; }
  .page.active { display:flex; flex-direction:column; }

  /* PAGE 1 */
  #page1 { align-items:center; justify-content:center; padding:60px 20px; }
  .card {
    background: var(--white); border-radius:4px;
    padding: 52px 48px; width:100%; max-width:540px;
    box-shadow: 0 4px 32px rgba(0,0,0,.08);
    border-top: 4px solid var(--teal);
  }
  .card-eyebrow { font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:3px; color:var(--teal); margin-bottom:12px; }
  .card h1 { font-size:26px; font-weight:900; color:var(--black); line-height:1.2; margin-bottom:8px; }
  .card p  { font-size:13px; color:var(--mid); margin-bottom:36px; line-height:1.7; font-weight:600; }
  .field { margin-bottom:18px; }
  .field label { display:block; font-size:10px; font-weight:800; color:var(--black); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px; }
  .field-row { display:flex; gap:14px; margin-bottom:18px; }
  .field-row .field { flex:1; margin-bottom:0; }
  .field input, .field select {
    width:100%; padding:13px 14px;
    background:var(--white); border:2px solid var(--border);
    border-radius:3px; color:var(--black); font-size:14px; font-weight:600;
    outline:none; transition:.2s; font-family:'Montserrat', sans-serif;
    -webkit-appearance:none; appearance:none;
  }
  .field input::placeholder { color:#ccc; font-weight:500; }
  .field input:focus, .field select:focus { border-color:var(--teal); }
  .field select option { color:var(--black); background:var(--white); }
  .select-wrap { position:relative; }
  .select-wrap::after { content:'▾'; position:absolute; right:14px; top:50%; transform:translateY(-50%); color:var(--mid); pointer-events:none; }
  .divider { border:none; border-top:1px solid var(--border); margin:24px 0; }
  .optional-hint { font-size:10px; color:var(--mid); font-weight:600; margin-top:6px; }
  .btn-primary {
    width:100%; padding:15px; background: var(--teal);
    border:none; border-radius:3px; color:var(--white); font-size:13px; font-weight:800;
    cursor:pointer; transition:.2s; margin-top:10px;
    letter-spacing:1.5px; text-transform:uppercase; font-family:'Montserrat', sans-serif;
  }
  .btn-primary:hover { background:var(--teal-d); }
  .no-lenders-msg {
    display:none; margin-top:14px; padding:12px 14px;
    background:#fff5f5; border:2px solid #ffcccc;
    border-radius:3px; color:#cc0000; font-size:12px;
    text-align:center; font-weight:700;
  }

  /* PAGE 2 */
  #page2 { padding:0; align-items:center; }
  .p2-inner { width:100%; max-width:700px; padding: 40px 20px 60px; }

  /* EMAIL SHELL */
  .email-shell { background:var(--white); border-radius:4px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,.12); }
  .email-body { padding:0 0 40px; font-size:15px; line-height:1.8; color:var(--black); }
  .email-header-strip {
    background: var(--black); padding:22px 32px;
    display:flex; align-items:center; justify-content:space-between; margin-bottom:32px;
  }
  .ehs-logo-wrap { display:flex; flex-direction:column; }
  .ehs-auto { font-size:8px; font-weight:800; letter-spacing:3px; color:rgba(255,255,255,.5); text-transform:uppercase; }
  .ehs-name { font-size:18px; font-weight:900; color:var(--white); letter-spacing:-.3px; }
  .ehs-name span { color:var(--teal); }
  .ehs-tag { font-size:10px; font-weight:800; color:var(--teal); border:1.5px solid var(--teal); padding:4px 10px; border-radius:2px; letter-spacing:1.5px; text-transform:uppercase; }
  .ebp { padding:0 32px; }
  .ebp p { margin-bottom:16px; color:#2d2d2d; font-size:14px; line-height:1.8; font-weight:500; }

  /* Stats */
  .stats-row { display:flex; gap:0; margin:24px 0; border:2px solid var(--teal); border-radius:3px; overflow:hidden; }
  .stat-item { flex:1; text-align:center; padding:18px 10px; border-right:1px solid var(--teal); }
  .stat-item:last-child { border-right:none; }
  .stat-num { font-size:22px; font-weight:900; color:var(--teal); }
  .stat-lbl { font-size:9px; font-weight:800; text-transform:uppercase; letter-spacing:1.2px; color:var(--mid); margin-top:4px; }

  /* Lenders */
  .lender-section { margin:20px 0; }
  .lender-card { display:flex; align-items:center; gap:14px; padding:12px 14px; border:1.5px solid var(--border); border-radius:3px; margin-bottom:6px; border-left:3px solid var(--teal); }
  .lender-dot { width:8px; height:8px; border-radius:50%; background:var(--teal); flex-shrink:0; }
  .lender-info .lname { font-weight:800; font-size:13px; color:var(--black); }
  .lender-info .lmeta { font-size:11px; color:var(--mid); margin-top:1px; font-weight:600; }
  .lender-badge { margin-left:auto; flex-shrink:0; font-size:9px; font-weight:800; text-transform:uppercase; letter-spacing:1px; padding:3px 10px; border-radius:2px; white-space:nowrap; background:rgba(0,200,180,.1); color:var(--teal); border:1px solid rgba(0,200,180,.3); }

  /* Features */
  .feature-list { margin:20px 0; }
  .feature-item { display:flex; align-items:flex-start; gap:12px; padding:10px 0; border-bottom:1px solid var(--border); }
  .feature-item:last-child { border-bottom:none; }
  .feature-icon { font-size:14px; flex-shrink:0; margin-top:2px; color:var(--teal); font-weight:900; }
  .feature-text .ftitle { font-weight:800; font-size:13px; color:var(--black); }
  .feature-text .fdesc  { font-size:12px; color:var(--mid); font-weight:600; margin-top:1px; }

  /* Dealers box */
  .dealers-box { background:#f9fffe; border:1.5px solid rgba(0,200,180,.3); border-left:3px solid var(--teal); border-radius:3px; padding:16px 18px; margin:20px 0; }
  .dealers-box-title { font-size:9px; font-weight:900; text-transform:uppercase; letter-spacing:2px; color:var(--teal); margin-bottom:10px; }
  .dealers-box ul { list-style:none; padding:0; margin:0; }
  .dealers-box ul li { font-size:13px; font-weight:600; color:#2d2d2d; padding:3px 0; }
  .dealers-box ul li::before { content:"\\2022  "; color:var(--teal); font-size:16px; vertical-align:middle; }
  .dealers-more { font-size:11px; font-weight:700; color:var(--mid); margin-top:6px; }

  /* Testimonials */
  .testimonial-block { margin:20px 0; }
  .testimonial { background:#fafafa; border-radius:3px; padding:14px 16px; margin-bottom:8px; border-left:3px solid var(--teal); }
  .testimonial p { font-size:13px; color:#333; font-weight:600; line-height:1.6; font-style:italic; margin:0; }
  .t-stars { font-size:11px; margin-top:6px; color:#f59e0b; }

  /* Budget table */
  .budget-table { width:100%; border-collapse:collapse; margin:20px 0; }
  .budget-table th { background:var(--black); color:var(--white); font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:1px; padding:10px 14px; text-align:left; }
  .budget-table td { padding:10px 14px; font-size:13px; font-weight:600; border-bottom:1px solid var(--border); color:#2d2d2d; }
  .budget-table tr:last-child td { border-bottom:none; }
  .budget-table td:first-child { font-weight:800; color:var(--black); }
  .rec-badge { font-size:9px; font-weight:800; text-transform:uppercase; letter-spacing:1px; padding:2px 8px; border-radius:2px; background:rgba(0,200,180,.1); color:var(--teal); border:1px solid rgba(0,200,180,.3); margin-left:6px; }

  /* CTA + Sig */
  .cta-block { margin:28px 0 8px; }
  .cta-sub { font-size:11px; color:var(--mid); margin-top:10px; font-weight:700; }
  .sig-block { margin-top:32px; padding-top:24px; border-top:2px solid var(--border); }
  .sig-name  { font-weight:900; font-size:14px; color:var(--black); }
  .sig-title { font-size:11px; color:var(--mid); margin-top:2px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }
  .sig-teal  { font-size:12px; color:var(--teal); margin-top:6px; font-weight:700; }
  .email-footer { text-align:center; padding:20px 32px; border-top:1px solid var(--border); font-size:10px; color:#aaa; font-weight:600; line-height:1.8; }

</style>
</head>
<body>

<!-- PAGE 1 -->
<div class="page active" id="page1">
  <div class="card" style="margin:auto;">
    <div class="card-eyebrow">Outreach Tool</div>
    <h1>Generate Your<br>Sales Email</h1>
    <p>Pick the email type, fill in the details, and get a ready-to-send email with local social proof in seconds.</p>

    <div class="field">
      <label>Email Type</label>
      <div class="select-wrap">
        <select id="emailType">
          <option value="fbmp">FBMP \u2014 Facebook Marketplace</option>
          <option value="ausa">A-USA \u2014 Financing / Lenders</option>
          <option value="da">DA \u2014 Digital Ads (Facebook Power Pack)</option>
        </select>
      </div>
    </div>

    <hr class="divider">

    <div class="field-row">
      <div class="field">
        <label>Your Name</label>
        <input type="text" id="repName" placeholder="e.g. Robert Anderson" />
      </div>
      <div class="field">
        <label>Your Phone</label>
        <input type="text" id="repPhone" placeholder="e.g. 469 489 1913" />
      </div>
    </div>

    <hr class="divider">

    <div class="field">
      <label>Dealer's First Name</label>
      <input type="text" id="dealerName" placeholder="e.g. Marcus" />
    </div>
    <div class="field">
      <label>Dealership Name</label>
      <input type="text" id="dealershipName" placeholder="e.g. Westside Auto" />
    </div>
    <div class="field-row">
      <div class="field" style="flex:1.4">
        <label>State</label>
        <div class="select-wrap">
          <select id="stateSelect">
            <option value="">— Select —</option>
            <option value="AZ">Arizona</option>
            <option value="AR">Arkansas</option>
            <option value="CA">California</option>
            <option value="CO">Colorado</option>
            <option value="CT">Connecticut</option>
            <option value="FL">Florida</option>
            <option value="GA">Georgia</option>
            <option value="ID">Idaho</option>
            <option value="IL">Illinois</option>
            <option value="IN">Indiana</option>
            <option value="KY">Kentucky</option>
            <option value="LA">Louisiana</option>
            <option value="MA">Massachusetts</option>
            <option value="MD">Maryland</option>
            <option value="ME">Maine</option>
            <option value="MI">Michigan</option>
            <option value="MN">Minnesota</option>
            <option value="MO">Missouri</option>
            <option value="MS">Mississippi</option>
            <option value="NC">North Carolina</option>
            <option value="ND">North Dakota</option>
            <option value="NJ">New Jersey</option>
            <option value="NV">Nevada</option>
            <option value="NY">New York</option>
            <option value="OH">Ohio</option>
            <option value="OK">Oklahoma</option>
            <option value="OR">Oregon</option>
            <option value="PA">Pennsylvania</option>
            <option value="RI">Rhode Island</option>
            <option value="SC">South Carolina</option>
            <option value="SD">South Dakota</option>
            <option value="TN">Tennessee</option>
            <option value="TX">Texas</option>
            <option value="UT">Utah</option>
            <option value="VA">Virginia</option>
            <option value="VT">Vermont</option>
            <option value="WA">Washington</option>
            <option value="WI">Wisconsin</option>
            <option value="WV">West Virginia</option>
          </select>
        </div>
      </div>
      <div class="field" style="flex:1">
        <label>City <span style="font-weight:600;text-transform:none;letter-spacing:0;color:var(--mid)">(optional)</span></label>
        <input type="text" id="cityInput" placeholder="e.g. Houston" />
      </div>
    </div>
    <div class="optional-hint">City pulls local dealer names as social proof when available.</div>

    <button class="btn-primary" onclick="generate()">Generate Email &#8594;</button>
    <div class="no-lenders-msg" id="noLendersMsg">&#9888; No lenders currently available in this state.</div>
  </div>
</div>

<!-- PAGE 2 -->
<div class="page" id="page2">
  <div class="p2-inner" style="margin:0 auto;">
    <div class="email-shell">
      <div class="email-body" id="emailBody"></div>
    </div>
  </div>
</div>

<script>
""")

html_parts.append("const CITY_DEALERS = ")
html_parts.append(city_data_js)
html_parts.append(";\n\n")
html_parts.append(LENDERS_JS)
html_parts.append("\n")
html_parts.append(STATE_NAMES_JS)
html_parts.append("""

function getLenders(st) {
  return LENDERS.filter(l => l.states.includes(st) || l.states.includes("ALL"));
}

function getCityDealers(city, st) {
  if (!city || !city.trim()) return null;
  const key = city.trim().replace(/\\b\\w/g, c => c.toUpperCase()) + '|' + st;
  return CITY_DEALERS[key] || null;
}

function headerHTML(tag) {
  return `
    <div class="email-header-strip">
      <div class="ehs-logo-wrap">
        <span class="ehs-auto">AUTO</span>
        <div class="ehs-name">DEALERS<span>.DIGITAL</span></div>
      </div>
      <div class="ehs-tag">${tag}</div>
    </div>`;
}

function sigHTML(repName, repPhone) {
  const n = repName  || 'Sales Representative';
  const p = repPhone || '';
  return `<div class="sig-block">
    <div class="sig-name">${n}</div>
    <div class="sig-title">Sales Representative &mdash; AutoDealers Digital</div>
    ${p ? `<div class="sig-teal">${p} &nbsp;&middot;&nbsp; autodealersdigital.com</div>` : `<div class="sig-teal">autodealersdigital.com</div>`}
  </div>`;
}

function dealersBoxHTML(city, st, intro) {
  const names = getCityDealers(city, st);
  if (!names || !names.length) return '';
  const display = names.slice(0, 8);
  const more    = names.length - display.length;
  const ct      = city.trim().replace(/\\b\\w/g, c => c.toUpperCase());
  const sn      = STATE_NAMES[st] || st;
  const title   = intro || `Already with us in ${ct}, ${sn}`;
  return `<div class="dealers-box">
    <div class="dealers-box-title">${title}</div>
    <ul>${display.map(n => `<li>${n}</li>`).join('')}</ul>
    ${more > 0 ? `<div class="dealers-more">+ ${more} more dealers in ${ct}</div>` : ''}
  </div>`;
}

function lenderCards(arr) {
  return arr.map(l => `
    <div class="lender-card">
      <div class="lender-dot"></div>
      <div class="lender-info">
        <div class="lname">${l.name}</div>
        <div class="lmeta">FICO ${l.fico} &nbsp;&middot;&nbsp; ${l.segment}</div>
      </div>
      <span class="lender-badge">${l.segment.split(' /')[0].split(' (')[0]}</span>
    </div>`).join('');
}

// ── FBMP ─────────────────────────────────────────────────
function buildFBMP(name, dealer, st, city, rep, phone) {
  const sn    = STATE_NAMES[st] || st;
  const ct    = city ? city.trim().replace(/\\b\\w/g, c => c.toUpperCase()) : '';
  const names = getCityDealers(city, st);
  const tel   = phone || '(305) 712-5672';

  let leadersHTML;
  if (names && names.length) {
    const d = names.slice(0, 6);
    const m = names.length - d.length;
    const loc = ct || sn;
    leadersHTML = `<div class="dealers-box">
      <div class="dealers-box-title">Join ${names.length} dealers already using us in ${loc}</div>
      <ul>${d.map(n => `<li>${n}</li>`).join('')}</ul>
      ${m > 0 ? `<div class="dealers-more">+ ${m} more dealers in the area</div>` : ''}
    </div>`;
  } else {
    leadersHTML = `<div class="dealers-box">
      <div class="dealers-box-title">Join the leaders</div>
      <ul>
        <li>Regional Auto Group</li><li>ZT Auto Group</li>
        <li>Philly Auto Group</li><li>Capital Motor Group</li>
      </ul>
    </div>`;
  }

  return `
    ${headerHTML('FB Marketplace')}
    <div class="ebp">
      <p>Hi ${name},</p>
      <p><strong>FB Marketplace automatic posting, AI lead conversion, and more!</strong><br>
      <span style="color:var(--teal);font-weight:800;">(Only $299 until May!)</span></p>
      <p>Facebook Marketplace is the most cost-effective lead-generation platform in the auto industry &mdash; and we&rsquo;ve automated it completely for over <strong>4,200+ dealers across the states.</strong></p>
      <p><strong>Our software does it all:</strong></p>
      <div class="feature-list">
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Auto-Post</div><div class="fdesc">Lists your inventory daily and automatically.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Auto-Refresh</div><div class="fdesc">Updates listings with the latest photos and prices.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Auto-Renew + Repost</div><div class="fdesc">Keeps your vehicles on top.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Auto-Delete</div><div class="fdesc">Removes sold units instantly.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Lead Exports</div><div class="fdesc">Sends every lead straight to your CRM.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">24/7 Automation</div><div class="fdesc">No downtime. No missed leads.</div></div></div>
      </div>
      <p>We don&rsquo;t stop at FB Marketplace! Your inventory also gets listed daily across <strong>20+ local FB car &amp; powersport groups</strong> &mdash; reaching thousands of buyers organically and without extra ad spend.</p>
      <p>And now, introducing <strong>AI automation:</strong><br>
      &bull; <strong>AI Lead Responder</strong> &mdash; Replies to every message 24/7 and captures contact info hands-free.<br>
      &bull; <strong>AI Lead Enrichment</strong> &mdash; Adds verified data (job title, income range, credit score band) from trusted sources.</p>
      ${leadersHTML}
      <p><strong>What dealers are saying:</strong></p>
      <div class="testimonial-block">
        <div class="testimonial"><p>&ldquo;Amazing support &mdash; our listings went live the same day and messages rolled in within hours.&rdquo;</p></div>
        <div class="testimonial"><p>&ldquo;Automation saves us 3 hours every morning. Best $299 we&rsquo;ve ever spent.&rdquo;</p><div class="t-stars">&#11088;&#11088;&#11088;&#11088;&#11088; Rated 4.9 / 5 from 380+ Google reviews</div></div>
      </div>
      <div class="cta-block">
        <div style="font-size:14px;font-weight:800;margin-bottom:8px;">Call or text <span style="color:var(--teal);">${tel}</span> to see how it works.</div>
        <div class="cta-sub">No contract &nbsp;&middot;&nbsp; No setup fees &nbsp;&middot;&nbsp; Cancel anytime</div>
      </div>
      ${sigHTML(rep, phone)}
    </div>
    <div class="email-footer">
      &copy; 2025 Auto Dealers Digital &nbsp;&middot;&nbsp; Serving 4,200+ dealers nationwide<br>
      <span style="font-size:9px;">If this isn&rsquo;t relevant for ${dealer}, just reply &ldquo;unsubscribe&rdquo; and I&rsquo;ll stop reaching out.</span>
    </div>`;
}

// ── A-USA ─────────────────────────────────────────────────
function buildAUSA(name, dealer, st, city, rep, phone) {
  const lenders = getLenders(st);
  const sn      = STATE_NAMES[st] || st;
  const box     = dealersBoxHTML(city, st, null);
  return `
    ${headerHTML('Lender Network')}
    <div class="ebp">
      <p>Hi ${name},</p>
      <p>We&rsquo;ve been working with a few dealerships in ${sn}, helping them access additional lenders and secure approvals they would normally lose.</p>
      <p>Most stores already have banks or credit unions in place. The reason they still add ours is simple: it gives them a backup when a deal doesn&rsquo;t fit their usual guidelines &mdash; instead of letting that customer walk.</p>
      <div class="stats-row">
        <div class="stat-item"><div class="stat-num">${lenders.length}</div><div class="stat-lbl">Lenders in ${sn}</div></div>
        <div class="stat-item"><div class="stat-num">$0</div><div class="stat-lbl">Recourse to Dealer</div></div>
        <div class="stat-item"><div class="stat-num">Soft</div><div class="stat-lbl">Pulls Only</div></div>
        <div class="stat-item"><div class="stat-num">No</div><div class="stat-lbl">Contracts</div></div>
      </div>
      <p>With our platform, <strong>${dealer}</strong> gets access to prime, subprime, and deep subprime lenders all in one place &mdash; no recourse and no risk to the dealership.</p>
      ${box}
      <p><strong>A few of our lenders currently active in ${sn}:</strong></p>
      <div class="lender-section">${lenderCards(lenders)}</div>
      <p>On top of that, we also help generate finance-ready buyers by automatically posting your inventory to Facebook Marketplace and 20 local buy-and-sell groups &mdash; sending those leads directly into your credit application.</p>
      <p>So it&rsquo;s one system that <strong>brings in the buyer, qualifies the lead, and gets them approved.</strong></p>
      <div class="cta-block">
        <div style="font-size:14px;font-weight:800;margin-bottom:8px;">Text or email for a demo${phone ? ' &mdash; <span style="color:var(--teal);">' + phone + '</span>' : ''}</div>
        <div class="cta-sub">No contracts &nbsp;&middot;&nbsp; No cancellation fees &nbsp;&middot;&nbsp; Cancel anytime</div>
      </div>
      ${sigHTML(rep, phone)}
    </div>`;
}

// ── DA ────────────────────────────────────────────────────
function buildDA(name, dealer, st, city, rep, phone) {
  return `
    ${headerHTML('Facebook Power Pack')}
    <div class="ebp">
      <p>Hi ${name},</p>
      <p>Thanks for your interest in the <strong>Facebook Power Pack!</strong> I&rsquo;m excited to walk you through what it offers and how we can make it work for <strong>${dealer}</strong>.</p>
      <p><strong>What Is a Facebook Carousel Lead Gen Campaign?</strong></p>
      <p>This is one of the top-performing ad formats in the Power Pack. Here&rsquo;s how it works:</p>
      <div class="feature-list">
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Real-Time Inventory Carousel</div><div class="fdesc">We run a carousel ad showing live inventory from your feed. Shoppers swipe through vehicles and click any model they like.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">In-App Lead Form</div><div class="fdesc">Buyers are taken to a lead form without ever leaving Facebook &mdash; no friction, higher conversion.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Instant CRM Delivery</div><div class="fdesc">You get their info instantly. Optionally redirect to a website of your choosing afterward.</div></div></div>
        <div class="feature-item"><div class="feature-icon">&#9654;</div><div class="feature-text"><div class="ftitle">Built for Mobile</div><div class="fdesc">Designed to drive ready-to-buy shoppers into your CRM with minimal effort on your end.</div></div></div>
      </div>
      <p><strong>Budget &amp; Fees</strong></p>
      <table class="budget-table">
        <tr><th>Weekly Budget</th><th>What You Get</th></tr>
        <tr><td>$250 / week</td><td>Entry-level presence. Great for testing targeting and maintaining visibility.</td></tr>
        <tr><td>$500 / week <span class="rec-badge">Recommended</span></td><td>Multiple ad types (Video, Banner, Carousel). Optimized for leads, not just clicks.</td></tr>
        <tr><td>$750 / week</td><td>Full campaign split by vehicle type or goal. Maximum reach &amp; lead quality.</td></tr>
      </table>
      <p><strong>Why Go Higher Than the Minimum?</strong></p>
      <p>&bull; Reach more in-market shoppers in your area<br>
      &bull; Run multiple ad types simultaneously (Video, Banner, and Carousel)<br>
      &bull; Optimize for leads, not just clicks &mdash; which improves ROI<br>
      &bull; Maximize Facebook&rsquo;s algorithm for better placement and engagement</p>
      <p>Let me know your thoughts, and if you have a budget range in mind, I&rsquo;d be happy to tailor a recommendation that gets the best results for what you invest.</p>
      <div class="cta-block">
        <div style="font-size:14px;font-weight:800;margin-bottom:8px;">Looking forward to hearing from you${phone ? ' &mdash; <span style="color:var(--teal);">' + phone + '</span>' : ''}</div>
        <div class="cta-sub">No contracts &nbsp;&middot;&nbsp; No cancellation fees &nbsp;&middot;&nbsp; Cancel anytime</div>
      </div>
      ${sigHTML(rep, phone)}
    </div>`;
}

// ── GENERATE ──────────────────────────────────────────────
function generate() {
  const type   = document.getElementById('emailType').value;
  const rep    = document.getElementById('repName').value.trim();
  const phone  = document.getElementById('repPhone').value.trim();
  const name   = document.getElementById('dealerName').value.trim();
  const dealer = document.getElementById('dealershipName').value.trim() || 'your dealership';
  const st     = document.getElementById('stateSelect').value;
  const city   = document.getElementById('cityInput').value.trim();
  const msg    = document.getElementById('noLendersMsg');

  if (!name)  { alert("Please enter the dealer's first name."); return; }
  if (!st)    { alert("Please select a state."); return; }
  if (!rep)   { alert("Please enter your name."); return; }
  msg.style.display = 'none';

  if (type === 'ausa' && !getLenders(st).length) {
    msg.style.display = 'block'; return;
  }

  let body = '';
  if      (type === 'fbmp') body = buildFBMP(name, dealer, st, city, rep, phone);
  else if (type === 'ausa') body = buildAUSA(name, dealer, st, city, rep, phone);
  else if (type === 'da')   body = buildDA  (name, dealer, st, city, rep, phone);

  document.getElementById('emailBody').innerHTML = body;
  document.getElementById('page1').classList.remove('active');
  document.getElementById('page2').classList.add('active');
  window.scrollTo(0, 0);
}

function goBack() {
  document.getElementById('page2').classList.remove('active');
  document.getElementById('page1').classList.add('active');
  window.scrollTo(0, 0);
}

</script>
</body>
</html>""")

output = ''.join(html_parts)
with open('c:/Users/pc/Desktop/Email/actives/emailfinancing.html', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Done. File size: {len(output):,} bytes ({len(output)//1024} KB)")
