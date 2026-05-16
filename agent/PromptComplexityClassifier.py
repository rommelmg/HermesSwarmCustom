import re
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    model: str
    score: int
    details: dict
    confidence: str


class PromptComplexityClassifier:
    LARGE_THRESHOLD  = 10
    MEDIUM_THRESHOLD = 5

    def __init__(self):
        flags = re.IGNORECASE

        # (raw_pattern, weight)
        _pattern_groups: dict[str, list[tuple[str, int]]] = {
            "simple": [
                (r"\bqué es\b|\bwhat (is|are)\b",                          -2),
                (r"\bquién (es|fue)\b|\bwho (is|was)\b",                   -2),
                (r"\bcuándo\b|\bwhen (was|is|did)\b",                      -1),
                (r"\bdefinición de\b|\bdefine\b|\bdefinition of\b",        -2),
                (r"\bsignifica\b|\bmeans?\b|\bmeaning of\b",               -1),
                (r"\btraduce\b|\btranslate\b",                             -1),
                (r"\bcómo se escribe\b|\bhow (do you )?spell\b",           -2),
                (r"\bcuál es la capital\b|\bwhat is the capital\b",        -2),
                (r"\blistar?\b|\benumera\b",                               -1),
                (r"\bcuántos?\b|\bhow many\b|\bhow much\b",               -1),
            ],
            "daily": [
                (r"\bredacta\b|\bescribe (un|el) (correo|email|mensaje|post|artículo)\b", 1),
                (r"\bresume\b|\bsummarize\b",                                1),
                (r"\btradu",                                                 1),
                (r"\borganiza\b|\bplanifica\b|\bschedule\b",                 1),
                (r"\bextrae\b|\bextract\b",                                  1),
                (r"\bdraft\b|\bwrite an? (email|message|post|article)\b",   1),
            ],
            "reasoning": [
                (r"\bpaso a paso\b|\bstep[- ]by[- ]step\b",                3),
                (r"\bexplica(r)? por qué\b|\bexplain why\b",               3),
                (r"\bjustif(y|ica)\b",                                      2),
                (r"\banaliz[ae]\b|\banalysis\b|\banalyze\b",               2),
                (r"\bderiv[ae]\b|\bderive\b",                               2),
                (r"\bdemuestra\b|\bprove\b|\bproof\b",                      2),
                (r"\binfiere\b|\binfer\b|\bdeduc[ei]\b",                    2),
                (r"\brazona\b|\breason through\b|\bthink through\b",        2),
                (r"\bdesglosa\b|\bbreak down\b",                            2),
                (r"\bcríticamente\b|\bcritically\b",                        2),
                (r"\bimplicaciones?\b|\bimplication(s)?\b",                 1),
                (r"\bcausal\b|\bcausa[sd]?\b|\bcause[sd]?\b",              1),
                (r"\bpor qué\b|\bwhy (does|is|are|would|should)\b",        1),
            ],
            "complex_task": [
                (r"\bdiseñ",                                                2),
                (r"\bdesign\b",                                             2),
                (r"\barquitectura\b|\barchitecture\b",                      2),
                (r"\bestrategia\b|\bstrateg",                               2),
                (r"\boptimiz",                                              2),
                (r"\bcompar",                                               2),
                (r"\bevalú|\beval[uú]",                                     2),
                (r"\bassess\b",                                             2),
                (r"\btrade[- ]?off\b",                                      2),
                (r"\bimplementa\b|\bimplement\b|\bconstruye\b",            2),
                (r"\bimplementación\b|\bimplementation\b",                  1),
                (r"\brefactor",                                             2),
                (r"\breestructura\b",                                       2),
                (r"\bdebug\b|\bdepura\b|\bdiagnose\b|\bdiagnostica\b",     1),
                (r"\bplani(fica|fy)\b|\bplanning\b",                       1),
                (r"\bsimul[ae]\b|\bsimulate\b",                            2),
                (r"\bpredic[et]\b|\bforecast\b",                           1),
                (r"\bpros (y contras|and cons)\b",                          2),
                (r"\bventajas y desventajas\b|\badvantages and disadvantages\b", 2),
                (r"\babstrae\b|\babstract\b|\bmodela\b|\bmodel\b",         1),
            ],
            "constraint": [
                (r"\bconsiderando\b|\bconsidering\b",                      1),
                (r"\bten en cuenta\b|\btake into account\b|\bbear in mind\b", 1),
                (r"\bwith the following\b|\bcon los? siguientes?\b",        1),
                (r"\bconstraints?\b|\brestricciones?\b|\blimitaciones?\b",  1),
                (r"\bdebe(n)? cumplir\b|\bmust (meet|satisfy|comply)\b",   1),
                (r"\bsujeto a\b|\bsubject to\b",                           1),
                (r"\bgarantizando\b|\bensuring\b|\bmaking sure\b",         1),
                (r"\brespetando\b|\brespecting\b|\badhering to\b",         1),
                (r"\bsin (exceder|sobrepasar)\b|\bwithout exceeding\b",    1),
                (r"\bbajo las condiciones\b|\bunder the conditions\b",     1),
            ],
            "math_science": [
                (r"\bintegral\b|\bderivada\b|\bderivative\b",              3),
                (r"\becuación diferencial\b|\bdifferential equation\b",    3),
                (r"\bcalcula\b|\bcalculate\b|\bcompute\b|\bsolve\b",       1),
                (r"\bformula\b|\bfórmula\b|\bdemostración\b",              2),
                (r"\bprobabilidad\b|\bprobability\b|\bstatistic\b",        2),
                (r"\bálgebra\b|\bcálculo\b|\bcalculus\b",                  2),
                (r"\bcomplejidad\b|\bcomplexity\b|\bbig[- ]?o\b",          2),
                (r"\bmatriz\b|\bmatrix\b|\bvector\b|\beigenvalue\b",       1),
                (r"\bregresión\b|\bregression\b|\bclasificación\b",        1),
            ],
            "code_technical": [
                (r"\bescribe (un[ao]?|el|la)?\s*(función|clase|script|programa|módulo)\b", 2),
                (r"\bwrite (a|an|the)?\s*(function|class|script|program|module)\b",        2),
                (r"\bimplementa (un[ao]?)?\s*(algoritmo|sistema|servicio|pipeline)\b",     2),
                (r"\balgorithm\b|\balgoritmo\b",                            2),
                (r"\bapi (rest|graphql|grpc)\b|\bmicroservice\b|\bmicroservicio\b",        2),
                (r"\bdistributed\b|\bdistribuido\b|\bconcurren",            2),
                (r"\bmachine learning\b|\bdeep learning\b|\bneural network\b|\bred neuronal\b", 2),
                (r"\bdatabase\b|\bbase de datos\b|\besquema de (base de datos|bd)\b", 1),
                (r"\bsecurity\b|\bseguridad\b|\bencrypt|\bencriptación\b",  1),
                (r"\bperformance\b|\brendimiento\b|\blatenc",               1),
                (r"\bci[/\-]?cd\b|\bdevops\b|\bdocker\b|\bkubernetes\b|\bk8s\b",         1),
                (r"\bsql\b|\bnosql\b|\borm\b|\bmigraci",                   1),
                (r"\bunit test\b|\btest unitario\b|\bintegration test\b",   1),
                (r"\bautenticaci|\bauthenticat",                            1),
            ],
            "multistep": [
                (r"\bprimero.{0,40}(luego|después|entonces)\b",            2),
                (r"\bfirst.{0,40}(then|after(ward)?|next)\b",              2),
                (r"\bpaso \d+\b|\bstep \d+\b",                             2),
                (r"\ba continuación\b|\bsubsequently\b",                    1),
                (r"\bfinalmente\b|\bfinally\b|\ben conclusión\b|\bin conclusion\b", 1),
                (r"\b(en )?(primer|segundo|tercer) lugar\b",               1),
                (r"\bin (the )?(first|second|third) place\b",              1),
            ],
            "hypothetical": [
                (r"\bqué (pasaría|ocurriría) si\b|\bwhat (if|would happen if)\b", 2),
                (r"\bhipotéticamente\b|\bhypothetically\b",                2),
                (r"\bescenario\b|\bscenario\b|\bcaso de estudio\b|\bcase study\b", 1),
                (r"\bsuponiendo que\b|\bassuming (that)?\b|\bgiven that\b", 1),
                (r"\bsi (fuera|hubiera|tuvieras?)\b|\bif (it were|there were|you had)\b", 1),
            ],
        }

        # Compile all patterns once at init
        self._groups: dict[str, list[tuple[re.Pattern, int]]] = {
            group: [(re.compile(pat, flags), w) for pat, w in items]
            for group, items in _pattern_groups.items()
        }

        self._list_re       = re.compile(r"\n[-*•]|\n\d+\.")
        self._code_block_re = re.compile(r"```|~~~")
        self._multi_q_re    = re.compile(r"\?.*\?", re.DOTALL)

    def _scan_group(self, group: str, text: str) -> tuple[int, int]:
        weight_sum, hits = 0, 0
        for pattern, weight in self._groups[group]:
            if pattern.search(text):
                weight_sum += weight
                hits += 1
        return weight_sum, hits

    def score(self, prompt: str) -> tuple[int, dict]:
        score   = 0
        details: dict = {}

        words = len(prompt.split())
        if words > 200:
            score += 3
            details["length"] = "very_long"
        elif words > 100:
            score += 2
            details["length"] = "long"
        elif words > 50:
            score += 1
            details["length"] = "medium"
        else:
            details["length"] = "short"

        for group in self._groups:
            w, hits = self._scan_group(group, prompt)
            score += w
            details[f"{group}_hits"] = hits

        if self._list_re.search(prompt):
            score += 2
            details["structured_list"] = True
        if self._code_block_re.search(prompt):
            score += 1
            details["code_block"] = True
        if self._multi_q_re.search(prompt):
            score += 2
            details["multiple_questions"] = True

        commas = prompt.count(",")
        if commas > 7:
            score += 2
            details["comma_density"] = "high"
        elif commas > 4:
            score += 1
            details["comma_density"] = "medium"

        return score, details

    def classify(self, prompt: str) -> ClassificationResult:
        score, details = self.score(prompt)
        effective = max(0, score)

        if effective >= self.LARGE_THRESHOLD:
            model      = "large_model"
            confidence = "high" if effective >= self.LARGE_THRESHOLD + 4 else "medium"
        elif effective >= self.MEDIUM_THRESHOLD:
            model      = "medium_model"
            confidence = "high" if effective >= self.MEDIUM_THRESHOLD + 2 else "medium"
        else:
            model      = "small_model"
            confidence = "high" if effective <= 1 else "medium"

        return ClassificationResult(
            model=model,
            score=score,
            details=details,
            confidence=confidence,
        )
