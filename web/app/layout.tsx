import type { Metadata } from "next";
import Script from "next/script";
import "./globals.css";

export const metadata: Metadata = {
  title: "MediSave • Same Medicine. A Fraction of the Price.",
  description:
    "Find verified Jan Aushadhi generic equivalents and see regulated prices before you buy.",
  openGraph: {
    title: "MediSave • Same Medicine. A Fraction of the Price.",
    description:
      "Find verified Jan Aushadhi generic equivalents and see regulated prices before you buy.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "MediSave • Same Medicine. A Fraction of the Price.",
    description:
      "Find verified Jan Aushadhi generic equivalents and see regulated prices before you buy.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html data-wf-domain="budgetrx.webflow.io" data-wf-page="6375a1fe1054d4bfd80053e6" data-wf-site="6375a1fe1054d4cf080053e5" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <link href="https://assets-global.website-files.com" rel="preconnect" crossOrigin="anonymous" />
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <link
          href="https://assets-global.website-files.com/6375a1fe1054d4cf080053e5/css/budgetrx.be30c3d13.min.css"
          rel="stylesheet"
          type="text/css"
        />
        <link
          href="https://cdn.prod.website-files.com/6375a1fe1054d4cf080053e5/63939ef58743daaf43f72287_favicon.png"
          rel="shortcut icon"
          type="image/x-icon"
        />
        <link
          href="https://cdn.prod.website-files.com/6375a1fe1054d4cf080053e5/63939ef90fc162a33c7d69dd_web-img.png"
          rel="apple-touch-icon"
        />
        <Script
          src="https://use.typekit.net/vzd3cvi.js"
          strategy="beforeInteractive"
        />
        <Script id="typekit-load" strategy="beforeInteractive">
          {`try{Typekit.load();}catch(e){}`}
        </Script>
        <Script id="wf-mod" strategy="beforeInteractive">
          {`!function(o,c){var n=c.documentElement,t=" w-mod-";n.className+=t+"js",("ontouchstart"in o||o.DocumentTouch&&c instanceof DocumentTouch)&&(n.className+=t+"touch")}(window,document);`}
        </Script>
        {/* jQuery */}
        <Script
          src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"
          strategy="beforeInteractive"
        />
        {/* BudgetRx inline app script */}
        <Script id="budgetrx-app" strategy="afterInteractive">{`
const MEDISAVE_DATA = [{"brand": "Dolo 650", "molecule": "Paracetamol", "strength": "650 mg", "form": "Tablet", "pack_size": "15", "mrp": 34.0, "ja": 10.5, "saving_pct": 69}, {"brand": "Crocin 650", "molecule": "Paracetamol", "strength": "650 mg", "form": "Tablet", "pack_size": "15", "mrp": 33.5, "ja": 10.5, "saving_pct": 69}, {"brand": "Calpol 500", "molecule": "Paracetamol", "strength": "500 mg", "form": "Tablet", "pack_size": "15", "mrp": 18.0, "ja": 7.0, "saving_pct": 61}, {"brand": "Augmentin 625 Duo", "molecule": "Amoxicillin and Clavulanic Acid", "strength": "500 mg + 125 mg", "form": "Tablet", "pack_size": "10", "mrp": 204.0, "ja": 52.0, "saving_pct": 75}, {"brand": "Clavam 625", "molecule": "Amoxicillin and Clavulanic Acid", "strength": "500 mg + 125 mg", "form": "Tablet", "pack_size": "10", "mrp": 201.0, "ja": 52.0, "saving_pct": 74}, {"brand": "Moxikind-CV 625", "molecule": "Amoxicillin and Clavulanic Acid", "strength": "500 mg + 125 mg", "form": "Tablet", "pack_size": "10", "mrp": 180.0, "ja": 52.0, "saving_pct": 71}, {"brand": "Pan 40", "molecule": "Pantoprazole", "strength": "40 mg", "form": "Tablet", "pack_size": "15", "mrp": 155.0, "ja": 15.0, "saving_pct": 90}, {"brand": "Pantocid 40", "molecule": "Pantoprazole", "strength": "40 mg", "form": "Tablet", "pack_size": "15", "mrp": 160.0, "ja": 15.0, "saving_pct": 91}, {"brand": "Pan-D", "molecule": "Pantoprazole + Domperidone", "strength": "40 mg + 30 mg", "form": "Capsule", "pack_size": "15", "mrp": 199.0, "ja": 28.0, "saving_pct": 86}, {"brand": "Pantop-DSR", "molecule": "Pantoprazole + Domperidone", "strength": "40 mg + 30 mg", "form": "Capsule", "pack_size": "10", "mrp": 145.0, "ja": 19.0, "saving_pct": 87}, {"brand": "Omez 20", "molecule": "Omeprazole", "strength": "20 mg", "form": "Capsule", "pack_size": "20", "mrp": 68.0, "ja": 9.0, "saving_pct": 87}, {"brand": "Razo 20", "molecule": "Rabeprazole", "strength": "20 mg", "form": "Tablet", "pack_size": "15", "mrp": 148.0, "ja": 16.5, "saving_pct": 89}, {"brand": "Atorva 10", "molecule": "Atorvastatin", "strength": "10 mg", "form": "Tablet", "pack_size": "15", "mrp": 98.0, "ja": 12.0, "saving_pct": 88}, {"brand": "Atorlip 20", "molecule": "Atorvastatin", "strength": "20 mg", "form": "Tablet", "pack_size": "15", "mrp": 185.0, "ja": 22.0, "saving_pct": 88}, {"brand": "Storvas 10", "molecule": "Atorvastatin", "strength": "10 mg", "form": "Tablet", "pack_size": "15", "mrp": 95.0, "ja": 12.0, "saving_pct": 87}, {"brand": "Rosuvas 10", "molecule": "Rosuvastatin", "strength": "10 mg", "form": "Tablet", "pack_size": "15", "mrp": 198.0, "ja": 25.0, "saving_pct": 87}, {"brand": "Rozavel 10", "molecule": "Rosuvastatin", "strength": "10 mg", "form": "Tablet", "pack_size": "10", "mrp": 140.0, "ja": 17.0, "saving_pct": 88}, {"brand": "Glycomet 500", "molecule": "Metformin", "strength": "500 mg", "form": "Tablet", "pack_size": "20", "mrp": 24.0, "ja": 7.0, "saving_pct": 71}, {"brand": "Glycomet-GP 1", "molecule": "Metformin + Glimepiride", "strength": "500 mg + 1 mg", "form": "Tablet", "pack_size": "15", "mrp": 85.0, "ja": 15.0, "saving_pct": 82}, {"brand": "Glycomet-GP 2", "molecule": "Metformin + Glimepiride", "strength": "500 mg + 2 mg", "form": "Tablet", "pack_size": "15", "mrp": 118.0, "ja": 19.0, "saving_pct": 84}, {"brand": "Jalra-M 50/500", "molecule": "Vildagliptin + Metformin", "strength": "50 mg + 500 mg", "form": "Tablet", "pack_size": "15", "mrp": 310.0, "ja": 42.0, "saving_pct": 86}, {"brand": "Telma 40", "molecule": "Telmisartan", "strength": "40 mg", "form": "Tablet", "pack_size": "15", "mrp": 138.0, "ja": 14.0, "saving_pct": 90}, {"brand": "Telmikind 40", "molecule": "Telmisartan", "strength": "40 mg", "form": "Tablet", "pack_size": "10", "mrp": 65.0, "ja": 9.5, "saving_pct": 85}, {"brand": "Telma-H", "molecule": "Telmisartan + Hydrochlorothiazide", "strength": "40 mg + 12.5 mg", "form": "Tablet", "pack_size": "15", "mrp": 188.0, "ja": 21.0, "saving_pct": 89}, {"brand": "Telma-AM", "molecule": "Telmisartan + Amlodipine", "strength": "40 mg + 5 mg", "form": "Tablet", "pack_size": "15", "mrp": 192.0, "ja": 22.0, "saving_pct": 89}, {"brand": "Amlokind 5", "molecule": "Amlodipine", "strength": "5 mg", "form": "Tablet", "pack_size": "15", "mrp": 35.0, "ja": 5.5, "saving_pct": 84}, {"brand": "Norvasc 5", "molecule": "Amlodipine", "strength": "5 mg", "form": "Tablet", "pack_size": "14", "mrp": 75.0, "ja": 5.0, "saving_pct": 93}, {"brand": "Azee 500", "molecule": "Azithromycin", "strength": "500 mg", "form": "Tablet", "pack_size": "5", "mrp": 132.0, "ja": 38.0, "saving_pct": 71}, {"brand": "Azithral 500", "molecule": "Azithromycin", "strength": "500 mg", "form": "Tablet", "pack_size": "5", "mrp": 130.0, "ja": 38.0, "saving_pct": 71}, {"brand": "Zithrox 500", "molecule": "Azithromycin", "strength": "500 mg", "form": "Tablet", "pack_size": "5", "mrp": 128.0, "ja": 38.0, "saving_pct": 70}, {"brand": "Montair-LC", "molecule": "Montelukast + Levocetirizine", "strength": "10 mg + 5 mg", "form": "Tablet", "pack_size": "10", "mrp": 198.0, "ja": 32.0, "saving_pct": 84}, {"brand": "Montek-LC", "molecule": "Montelukast + Levocetirizine", "strength": "10 mg + 5 mg", "form": "Tablet", "pack_size": "10", "mrp": 190.0, "ja": 32.0, "saving_pct": 83}, {"brand": "Cetzine 10", "molecule": "Cetirizine", "strength": "10 mg", "form": "Tablet", "pack_size": "10", "mrp": 22.0, "ja": 4.5, "saving_pct": 80}, {"brand": "Allegra 120", "molecule": "Fexofenadine", "strength": "120 mg", "form": "Tablet", "pack_size": "10", "mrp": 175.0, "ja": 29.0, "saving_pct": 83}, {"brand": "Combiflam", "molecule": "Ibuprofen + Paracetamol", "strength": "400 mg + 325 mg", "form": "Tablet", "pack_size": "20", "mrp": 46.0, "ja": 12.0, "saving_pct": 74}, {"brand": "Zerodol-P", "molecule": "Aceclofenac + Paracetamol", "strength": "100 mg + 325 mg", "form": "Tablet", "pack_size": "10", "mrp": 68.0, "ja": 14.0, "saving_pct": 79}, {"brand": "Shelcal 500", "molecule": "Calcium + Vitamin D3", "strength": "500 mg + 250 IU", "form": "Tablet", "pack_size": "15", "mrp": 135.0, "ja": 25.0, "saving_pct": 81}, {"brand": "Cipcal 500", "molecule": "Calcium + Vitamin D3", "strength": "500 mg + 250 IU", "form": "Tablet", "pack_size": "15", "mrp": 120.0, "ja": 25.0, "saving_pct": 79}, {"brand": "Thyronorm 50", "molecule": "Thyroxine Sodium", "strength": "50 mcg", "form": "Tablet", "pack_size": "120", "mrp": 180.0, "ja": 45.0, "saving_pct": 75}, {"brand": "Eltroxin 50", "molecule": "Thyroxine Sodium", "strength": "50 mcg", "form": "Tablet", "pack_size": "120", "mrp": 175.0, "ja": 45.0, "saving_pct": 74}];

function initMediSaveSearch() {
  if (typeof window.$ === 'undefined') {
    setTimeout(initMediSaveSearch, 50);
    return;
  }

  $('#drug-form').submit(function(e) { e.preventDefault(); });

  $('input#drug-search').on('input keyup', function() {
    const q = $(this).val().trim().toLowerCase();
    const container = $('#autofill-container');
    container.empty();

    if (q.length < 2) return;

    const results = MEDISAVE_DATA.filter(m =>
      m.brand.toLowerCase().includes(q) ||
      m.molecule.toLowerCase().includes(q) ||
      m.strength.toLowerCase().includes(q)
    ).slice(0, 8);

    if (results.length === 0) {
      container.append('<div style="padding:14px; color:#575279; font-size:14px; background:#FFFFFF; border-radius:12px; margin-top:8px; border:1px solid #E4E5DD;">Not found in our data, ask your pharmacist or doctor.</div>');
      return;
    }

    results.forEach(drug => {
      const clone = $('#autofill-entry').clone();
      clone.css('display', 'flex');
      clone.find('#autofill-value').html('<strong>' + drug.brand + '</strong> <span style="font-size:13px; color:#575279;">(' + drug.molecule + ' ' + drug.strength + ')</span>');
      clone.find('.autofill-button_text').html('<span style="color:#1FAE6B; font-weight:800; font-size:14px;">₹' + drug.ja + '</span> <span style="text-decoration:line-through; color:#575279; font-size:12px;">₹' + drug.mrp + '</span> <span style="background:#A6D63A; color:#1B0A66; padding:2px 8px; border-radius:999px; font-weight:800; font-size:11px; margin-left:6px;">Save ' + drug.saving_pct + '%</span>');
      clone.find('#autofill-package-size').text(drug.pack_size);
      clone.find('#autofill-package-size-label').text(drug.form + 's');

      clone.click(function() {
        alert('Selected: ' + drug.brand + '
Active Molecule: ' + drug.molecule + ' (' + drug.strength + ')
Brand MRP: ₹' + drug.mrp + '
Jan Aushadhi Price: ₹' + drug.ja + ' (' + drug.saving_pct + '% Savings)

Price and molecule information only, not medical advice. Confirm with your doctor or pharmacist.');
      });

      container.append(clone);
    });
  });
}

if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMediSaveSearch);
  } else {
    initMediSaveSearch();
  }
}
`}</Script>
        {/* Webflow JS */}
        <Script
          src="https://assets-global.website-files.com/6375a1fe1054d4cf080053e5/js/budgetrx.ba14818d5.js"
          strategy="afterInteractive"
        />
      </head>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
