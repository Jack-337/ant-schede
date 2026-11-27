// Costruisce il catalogo completo degli esercizi Garmin per l'app
// Fonti: profilo ufficiale FIT SDK (codici), dati Garmin Connect (nomi inglesi, muscoli, attrezzi)
import { Profile } from "@garmin/fitsdk";
import { readFileSync, writeFileSync } from "node:fs";
import { IT, CAT_IT, SKIP_CATS, MUSCLES, MUSCLES_IT, CAT_MUSCLES, EQUIP, GLOSS } from "./it-names.mjs";
import { STRETCH, PRESETS } from "./stretch-lib.mjs";
for (const [fit, , it] of STRETCH) IT["warmUp." + fit] = it;

// Dati Garmin Connect: clonare https://github.com/maximecharriere/GarminExercisesCollector e indicare la cartella examples_garmin_data
const D = (process.env.GARMIN_DATA || "../../GarminExercisesCollector/examples_garmin_data") + "/";
const T = Profile.types;
const UP = (s) => s.replace(/([a-z0-9])([A-Z])/g, "$1_$2").replace(/([A-Z])([A-Z][a-z])/g, "$1_$2").toUpperCase();
const tr = {};
for (const l of readFileSync(D + "translation_exercise_types.txt", "utf8").split("\n")) { const i = l.indexOf("="); if (i > 0) tr[l.slice(0, i)] = l.slice(i + 1).trim(); }
const muscles = JSON.parse(readFileSync(D + "Exercises.json", "utf8")).categories;
const equip = {};
for (const c of JSON.parse(readFileSync(D + "exerciseToEquipments.json", "utf8"))) for (const e of c.exercisesInCategory) equip[c.exerciseCategoryKey + "/" + e.exerciseKey] = e;
const human = (n) => n.replace(/([a-z0-9])([A-Z])/g, "$1 $2").replace(/^./, (c) => c.toUpperCase());
const EQ_GROUPS = [...new Set(Object.values(EQUIP))];
const mask = (list) => list.reduce((m, k) => (MUSCLES.indexOf(k) >= 0 ? m | (1 << MUSCLES.indexOf(k)) : m), 0);

const cats = [], out = [];
const usedIT = new Set();
let withMuscles = 0;
for (const [catCode, cat] of Object.entries(T.exerciseCategory)) {
  if (SKIP_CATS.has(cat)) continue;
  const table = T[cat + "ExerciseName"]; if (!table) continue;
  const ci = cats.push({ k: cat, it: CAT_IT[cat] || human(cat), en: tr["category_type_" + UP(cat)] || human(cat) }) - 1;
  for (const [code, name] of Object.entries(table)) {
    if (/wheelchair/i.test(name)) continue;
    const key = UP(cat) + "/" + UP(name);
    const en = tr["exercise_type_" + UP(name)] || human(name);
    const m = muscles[UP(cat)]?.exercises?.[UP(name)] || equip[key];
    let p, s;
    if (m && (m.primaryMuscles.length || m.secondaryMuscles.length)) { p = m.primaryMuscles; s = m.secondaryMuscles; withMuscles++; }
    else [p, s] = CAT_MUSCLES[cat] || [[], []];
    const eqs = [...new Set((equip[key]?.equipmentKeys || []).map((k) => EQUIP[k]).filter(Boolean))].map((g) => EQ_GROUPS.indexOf(g));
    const it = IT[cat + "." + name] || "";
    if (it) usedIT.add(cat + "." + name);
    out.push([Number(catCode), Number(code), en, it, ci, mask(p), mask(s), eqs.reduce((a, i) => a | (1 << i), 0)]);
  }
}
const missingIT = Object.keys(IT).filter((k) => !usedIT.has(k));
if (missingIT.length) { console.log("Nomi italiani senza esercizio:", missingIT.join(", ")); process.exit(1); }
const wuCat = Number(Object.keys(T.exerciseCategory).find((k) => T.exerciseCategory[k] === "warmUp"));
const stretch = STRETCH.map(([fit, img, it, dyn, side, mus]) => ({ c: wuCat, e: Number(Object.keys(T.warmUpExerciseName).find((k) => T.warmUpExerciseName[k] === fit)), k: fit, img: img.replace(/[^A-Za-z0-9]/g, "_"), dyn, side, m: mus.reduce((a, i) => a | (1 << i), 0) }));
writeFileSync("catalog-full.json", JSON.stringify({ cats, muscles: MUSCLES_IT, eq: EQ_GROUPS, gloss: GLOSS, ex: out, stretch, presets: PRESETS }));
console.log("OK esercizi:", out.length, "categorie:", cats.length, "con muscoli Garmin:", withMuscles, "nomi IT:", usedIT.size, "KB:", (JSON.stringify(out).length / 1024).toFixed(0));
