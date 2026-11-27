// Rilegge il file FIT con il decoder ufficiale per verificarne la validità
import { Decoder, Stream } from "@garmin/fitsdk";
import { readFileSync } from "node:fs";

const d = new Decoder(Stream.fromByteArray(readFileSync(process.argv[2])));
console.log("isFIT:", d.isFIT(), "integrity:", d.checkIntegrity());
const { messages, errors } = d.read();
console.log("errors:", errors);
console.log(messages.fileIdMesgs, messages.workoutMesgs);
console.table(messages.workoutStepMesgs.map((s) => ({ i: s.messageIndex, nome: s.wktStepName, tipo: s.durationType, rep: s.durationReps, sec: s.durationTime, step: s.durationStep, serie: s.repeatSteps ?? s.targetValue, kg: s.exerciseWeight, int: s.intensity, cat: s.exerciseCategory, ex: s.exerciseName })));
console.table(messages.exerciseTitleMesgs);
