# Report Tables

This document compiles the experiment tables that support the final report.

## Ablation Table
| case_id | user_text | alpha | text_top_emotion | text_top_probability | face_top_emotion | face_top_probability | fused_top_emotion | fused_top_probability | text_only_top_emotion | face_only_top_emotion | empathetic_response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | I am really happy with how this turned out. | 0.5 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | happy | neutral | Understood. I will stay focused and supportive. |
| 2 | Today felt rough and I am still sad about it. | 0.5 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | sad | neutral | Understood. I will stay focused and supportive. |
| 3 | I am frustrated because the system keeps failing. | 0.5 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.435 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.5 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.679047619047619 | neutral | neutral | That seems steady. I can help with the next step. |
| 5 | I am nervous about the presentation tomorrow. | 0.5 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | fear | neutral | I am getting a neutral signal, so I will keep this practical. |
| 6 | Wow, I did not expect that result at all. | 0.5 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.4515094339622642 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.5 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | disgust | neutral | Understood. I will stay focused and supportive. |
| 8 | I am excited and relieved after finishing the task. | 0.5 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.4156338028169014 | happy | neutral | Thanks for sharing. I will keep this clear and concise. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.5 | neutral | 0.5 | neutral | 0.62 | neutral | 0.56 | neutral | neutral | Thanks for sharing. I will keep this clear and concise. |
| 10 | I am angry, but also a little worried about what comes next. | 0.5 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.4003614457831325 | angry | neutral | Thanks for sharing. I will keep this clear and concise. |
| 11 | The meeting was fine and nothing unusual happened. | 0.5 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6250684931506849 | neutral | neutral | Understood. I will stay focused and supportive. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.5 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.441578947368421 | sad | neutral | I am getting a neutral signal, so I will keep this practical. |

## Alpha Sensitivity Table
| case_id | user_text | alpha | text_top_emotion | text_top_probability | face_top_emotion | face_top_probability | fused_top_emotion | fused_top_probability | text_only_top_emotion | face_only_top_emotion | empathetic_response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | I am really happy with how this turned out. | 0.0 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.62 | happy | neutral | Understood. I will stay focused and supportive. |
| 2 | Today felt rough and I am still sad about it. | 0.0 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.62 | sad | neutral | Understood. I will stay focused and supportive. |
| 3 | I am frustrated because the system keeps failing. | 0.0 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.62 | angry | neutral | That seems steady. I can help with the next step. |
| 4 | I feel okay, just checking in for now. | 0.0 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.62 | neutral | neutral | That seems steady. I can help with the next step. |
| 5 | I am nervous about the presentation tomorrow. | 0.0 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.62 | fear | neutral | That seems steady. I can help with the next step. |
| 6 | Wow, I did not expect that result at all. | 0.0 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.62 | surprise | neutral | That seems steady. I can help with the next step. |
| 7 | That smelled gross and made me uncomfortable. | 0.0 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.62 | disgust | neutral | Thanks for sharing. I will keep this clear and concise. |
| 8 | I am excited and relieved after finishing the task. | 0.0 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.62 | happy | neutral | That seems steady. I can help with the next step. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.0 | neutral | 0.5 | neutral | 0.62 | neutral | 0.62 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.0 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.62 | angry | neutral | Understood. I will stay focused and supportive. |
| 11 | The meeting was fine and nothing unusual happened. | 0.0 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.62 | neutral | neutral | That seems steady. I can help with the next step. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.0 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.62 | sad | neutral | Thanks for sharing. I will keep this clear and concise. |
| 1 | I am really happy with how this turned out. | 0.25 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.5264754098360656 | happy | neutral | Understood. I will stay focused and supportive. |
| 2 | Today felt rough and I am still sad about it. | 0.25 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.5264754098360656 | sad | neutral | Thanks for sharing. I will keep this clear and concise. |
| 3 | I am frustrated because the system keeps failing. | 0.25 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.5275 | angry | neutral | I am getting a neutral signal, so I will keep this practical. |
| 4 | I feel okay, just checking in for now. | 0.25 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.6495238095238095 | neutral | neutral | That seems steady. I can help with the next step. |
| 5 | I am nervous about the presentation tomorrow. | 0.25 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.5296551724137931 | fear | neutral | Understood. I will stay focused and supportive. |
| 6 | Wow, I did not expect that result at all. | 0.25 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.5357547169811321 | surprise | neutral | I am getting a neutral signal, so I will keep this practical. |
| 7 | That smelled gross and made me uncomfortable. | 0.25 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.5296551724137931 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.25 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.5178169014084507 | happy | neutral | Understood. I will stay focused and supportive. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.25 | neutral | 0.5 | neutral | 0.62 | neutral | 0.59 | neutral | neutral | Thanks for sharing. I will keep this clear and concise. |
| 10 | I am angry, but also a little worried about what comes next. | 0.25 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.5101807228915662 | angry | neutral | Thanks for sharing. I will keep this clear and concise. |
| 11 | The meeting was fine and nothing unusual happened. | 0.25 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6225342465753424 | neutral | neutral | That seems steady. I can help with the next step. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.25 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.5307894736842105 | sad | neutral | I am getting a neutral signal, so I will keep this practical. |
| 1 | I am really happy with how this turned out. | 0.5 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | happy | neutral | Thanks for sharing. I will keep this clear and concise. |
| 2 | Today felt rough and I am still sad about it. | 0.5 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | sad | neutral | Understood. I will stay focused and supportive. |
| 3 | I am frustrated because the system keeps failing. | 0.5 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.435 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.5 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.679047619047619 | neutral | neutral | That seems steady. I can help with the next step. |
| 5 | I am nervous about the presentation tomorrow. | 0.5 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | fear | neutral | Thanks for sharing. I will keep this clear and concise. |
| 6 | Wow, I did not expect that result at all. | 0.5 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.4515094339622642 | surprise | neutral | I am getting a neutral signal, so I will keep this practical. |
| 7 | That smelled gross and made me uncomfortable. | 0.5 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | disgust | neutral | I am getting a neutral signal, so I will keep this practical. |
| 8 | I am excited and relieved after finishing the task. | 0.5 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.4156338028169014 | happy | neutral | Understood. I will stay focused and supportive. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.5 | neutral | 0.5 | neutral | 0.62 | neutral | 0.56 | neutral | neutral | I am getting a neutral signal, so I will keep this practical. |
| 10 | I am angry, but also a little worried about what comes next. | 0.5 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.4003614457831325 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.5 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6250684931506849 | neutral | neutral | That seems steady. I can help with the next step. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.5 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.441578947368421 | sad | neutral | Understood. I will stay focused and supportive. |
| 1 | I am really happy with how this turned out. | 0.75 | happy | 0.4262295081967213 | neutral | 0.62 | happy | 0.3396721311475409 | happy | neutral | Nice, that reads as a good moment. |
| 2 | Today felt rough and I am still sad about it. | 0.75 | sad | 0.4262295081967213 | neutral | 0.62 | sad | 0.3396721311475409 | sad | neutral | That seems difficult. Let us focus on one small next step. |
| 3 | I am frustrated because the system keeps failing. | 0.75 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.3425 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.75 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.7085714285714285 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 0.75 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.3489655172413793 | fear | neutral | I am getting a neutral signal, so I will keep this practical. |
| 6 | Wow, I did not expect that result at all. | 0.75 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.3672641509433962 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.75 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.3489655172413793 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.75 | happy | 0.5070422535211268 | neutral | 0.62 | happy | 0.4002816901408451 | happy | neutral | That sounds positive. I am glad it is going well. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.75 | neutral | 0.5 | neutral | 0.62 | neutral | 0.53 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.75 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.2905421686746987 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.75 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6276027397260274 | neutral | neutral | I am getting a neutral signal, so I will keep this practical. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.75 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.3523684210526315 | sad | neutral | That seems steady. I can help with the next step. |
| 1 | I am really happy with how this turned out. | 1.0 | happy | 0.4262295081967213 | neutral | 0.62 | happy | 0.4262295081967213 | happy | neutral | That sounds positive. I am glad it is going well. |
| 2 | Today felt rough and I am still sad about it. | 1.0 | sad | 0.4262295081967213 | neutral | 0.62 | sad | 0.4262295081967213 | sad | neutral | I am sorry this feels hard. We can take it step by step. |
| 3 | I am frustrated because the system keeps failing. | 1.0 | angry | 0.4166666666666667 | neutral | 0.62 | angry | 0.4166666666666667 | angry | neutral | That sounds tense. We can work through it carefully. |
| 4 | I feel okay, just checking in for now. | 1.0 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.738095238095238 | neutral | neutral | Thanks for sharing. I will keep this clear and concise. |
| 5 | I am nervous about the presentation tomorrow. | 1.0 | fear | 0.396551724137931 | neutral | 0.62 | fear | 0.396551724137931 | fear | neutral | I can help reduce uncertainty by breaking this down. |
| 6 | Wow, I did not expect that result at all. | 1.0 | surprise | 0.3396226415094339 | neutral | 0.62 | surprise | 0.3396226415094339 | surprise | neutral | Interesting. We can make sense of it together. |
| 7 | That smelled gross and made me uncomfortable. | 1.0 | disgust | 0.396551724137931 | neutral | 0.62 | disgust | 0.396551724137931 | disgust | neutral | I hear discomfort there. Let us move toward something more workable. |
| 8 | I am excited and relieved after finishing the task. | 1.0 | happy | 0.5070422535211268 | neutral | 0.62 | happy | 0.5070422535211268 | happy | neutral | That sounds positive. I am glad it is going well. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 1.0 | neutral | 0.5 | neutral | 0.62 | neutral | 0.5 | neutral | neutral | Understood. I will stay focused and supportive. |
| 10 | I am angry, but also a little worried about what comes next. | 1.0 | angry | 0.325301204819277 | neutral | 0.62 | angry | 0.325301204819277 | angry | neutral | I can see frustration here. Let us slow it down. |
| 11 | The meeting was fine and nothing unusual happened. | 1.0 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6301369863013698 | neutral | neutral | Understood. I will stay focused and supportive. |
| 12 | I feel a bit disappointed, but I can recover from it. | 1.0 | sad | 0.3859649122807018 | neutral | 0.62 | sad | 0.3859649122807018 | sad | neutral | I hear some sadness. We can keep moving gently. |

## Case Study Table
| case_id | user_text | text_top_emotion | face_top_emotion | fused_top_emotion | empathetic_response | case_type |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | I am thrilled with the result and feel genuinely happy. | happy | happy | happy | Nice, that reads as a good moment. | Congruent |
| 2 | I feel sad and drained after losing the opportunity. | sad | sad | sad | That seems difficult. Let us focus on one small next step. | Congruent |
| 3 | I am furious that the system keeps crashing. | angry | angry | angry | I can see frustration here. Let us slow it down. | Congruent |
| 4 | I am nervous about the interview tomorrow. | fear | fear | fear | That sounds uncertain. I can help make the next step feel safer. | Congruent |
| 5 | Wow, I did not expect that announcement at all. | surprise | surprise | surprise | Interesting. We can make sense of it together. | Congruent |
| 6 | I am thrilled with the result, but the room felt gloomy to me. | neutral | sad | neutral | Thanks for sharing. I will keep this clear and concise. | Dissonant |
| 7 | I feel sad and drained after losing the opportunity, even though everyone looks upbeat. | sad | happy | happy | I am picking up a positive tone here. | Dissonant |
| 8 | I am angry about the delay, but the room feels calm and neutral. | angry | neutral | neutral | Thanks for sharing. I will keep this clear and concise. | Dissonant |
| 9 | I am okay, just checking in and moving through the day. | neutral | neutral | neutral | That seems steady. I can help with the next step. | Ambiguous |
| 10 | Part of me feels hopeful, part of me feels tired. | neutral | neutral | neutral | I am getting a neutral signal, so I will keep this practical. | Ambiguous |

## Mode Comparison Table
| case_id | user_text | text_top_emotion | face_top_emotion | fused_top_emotion | text_only_response | face_only_response | fused_response | case_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | I am thrilled with the result and feel genuinely happy. | happy | happy | happy | That sounds positive. I am glad it is going well. | That sounds positive. I am glad it is going well. | That sounds positive. I am glad it is going well. | Congruent |
| 2 | I feel sad and drained after losing the opportunity. | sad | sad | sad | That seems difficult. Let us focus on one small next step. | That sounds heavy. I am here to help make it easier. | That sounds heavy. I am here to help make it easier. | Congruent |
| 3 | I am furious that the system keeps crashing. | angry | angry | angry | I hear the frustration. I will keep this calm and direct. | I hear the frustration. I will keep this calm and direct. | That feels heated. We can make the next step more manageable. | Congruent |
| 4 | I am nervous about the interview tomorrow. | fear | fear | fear | That sounds uncertain. I can help make the next step feel safer. | That seems a little tense. We can slow down and clarify it. | I hear some worry. Let us make this feel more manageable. | Congruent |
| 5 | Wow, I did not expect that announcement at all. | surprise | surprise | surprise | Interesting. We can make sense of it together. | That feels unexpected. I can help unpack it. | That seems a bit sudden. I can help sort through it. | Congruent |
| 6 | I am thrilled with the result, but the room felt gloomy to me. | neutral | sad | neutral | Understood. I will stay focused and supportive. | I am sorry this feels hard. We can take it step by step. | Understood. I will stay focused and supportive. | Dissonant |
| 7 | I feel sad and drained after losing the opportunity, even though everyone looks upbeat. | sad | happy | happy | That seems difficult. Let us focus on one small next step. | That sounds positive. I am glad it is going well. | Nice, that reads as a good moment. | Dissonant |
| 8 | I am angry about the delay, but the room feels calm and neutral. | angry | neutral | neutral | That sounds tense. We can work through it carefully. | Understood. I will stay focused and supportive. | Understood. I will stay focused and supportive. | Dissonant |
| 9 | I am okay, just checking in and moving through the day. | neutral | neutral | neutral | Understood. I will stay focused and supportive. | That seems steady. I can help with the next step. | Understood. I will stay focused and supportive. | Ambiguous |
| 10 | Part of me feels hopeful, part of me feels tired. | neutral | neutral | neutral | Thanks for sharing. I will keep this clear and concise. | That seems steady. I can help with the next step. | That seems steady. I can help with the next step. | Ambiguous |

## Human Evaluation Summary Table
_No rows available yet._
