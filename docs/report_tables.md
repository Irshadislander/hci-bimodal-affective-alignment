# Report Tables

This document compiles the experiment tables that support the final report.

## Ablation Table
| case_id | user_text | alpha | text_top_emotion | text_top_probability | face_top_emotion | face_top_probability | fused_top_emotion | fused_top_probability | text_only_top_emotion | face_only_top_emotion | empathetic_response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | I am really happy with how this turned out. | 0.5 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | happy | neutral | That seems steady. I can help with the next step. |
| 2 | Today felt rough and I am still sad about it. | 0.5 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | sad | neutral | This reads as neutral, so I will keep the response practical. |
| 3 | I am frustrated because the system keeps failing. | 0.5 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.435 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.5 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.679047619047619 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 0.5 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | fear | neutral | This reads as neutral, so I will keep the response practical. |
| 6 | Wow, I did not expect that result at all. | 0.5 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.4515094339622642 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.5 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.5 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.4156338028169014 | happy | neutral | That seems steady. I can help with the next step. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.5 | neutral | 0.5 | neutral | 0.62 | neutral | 0.56 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.5 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.4003614457831325 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.5 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6250684931506849 | neutral | neutral | Thanks for sharing. I will keep things straightforward. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.5 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.441578947368421 | sad | neutral | That seems steady. I can help with the next step. |

## Alpha Sensitivity Table
| case_id | user_text | alpha | text_top_emotion | text_top_probability | face_top_emotion | face_top_probability | fused_top_emotion | fused_top_probability | text_only_top_emotion | face_only_top_emotion | empathetic_response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | I am really happy with how this turned out. | 0.0 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.62 | happy | neutral | That seems steady. I can help with the next step. |
| 2 | Today felt rough and I am still sad about it. | 0.0 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.62 | sad | neutral | This reads as neutral, so I will keep the response practical. |
| 3 | I am frustrated because the system keeps failing. | 0.0 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.62 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.0 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.62 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 0.0 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.62 | fear | neutral | This reads as neutral, so I will keep the response practical. |
| 6 | Wow, I did not expect that result at all. | 0.0 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.62 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.0 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.62 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.0 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.62 | happy | neutral | That seems steady. I can help with the next step. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.0 | neutral | 0.5 | neutral | 0.62 | neutral | 0.62 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.0 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.62 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.0 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.62 | neutral | neutral | Thanks for sharing. I will keep things straightforward. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.0 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.62 | sad | neutral | That seems steady. I can help with the next step. |
| 1 | I am really happy with how this turned out. | 0.25 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.5264754098360656 | happy | neutral | That seems steady. I can help with the next step. |
| 2 | Today felt rough and I am still sad about it. | 0.25 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.5264754098360656 | sad | neutral | This reads as neutral, so I will keep the response practical. |
| 3 | I am frustrated because the system keeps failing. | 0.25 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.5275 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.25 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.6495238095238095 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 0.25 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.5296551724137931 | fear | neutral | This reads as neutral, so I will keep the response practical. |
| 6 | Wow, I did not expect that result at all. | 0.25 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.5357547169811321 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.25 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.5296551724137931 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.25 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.5178169014084507 | happy | neutral | That seems steady. I can help with the next step. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.25 | neutral | 0.5 | neutral | 0.62 | neutral | 0.59 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.25 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.5101807228915662 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.25 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6225342465753424 | neutral | neutral | Thanks for sharing. I will keep things straightforward. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.25 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.5307894736842105 | sad | neutral | That seems steady. I can help with the next step. |
| 1 | I am really happy with how this turned out. | 0.5 | happy | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | happy | neutral | That seems steady. I can help with the next step. |
| 2 | Today felt rough and I am still sad about it. | 0.5 | sad | 0.4262295081967213 | neutral | 0.62 | neutral | 0.4329508196721311 | sad | neutral | This reads as neutral, so I will keep the response practical. |
| 3 | I am frustrated because the system keeps failing. | 0.5 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.435 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.5 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.679047619047619 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 0.5 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | fear | neutral | This reads as neutral, so I will keep the response practical. |
| 6 | Wow, I did not expect that result at all. | 0.5 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.4515094339622642 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.5 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.4393103448275862 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.5 | happy | 0.5070422535211268 | neutral | 0.62 | neutral | 0.4156338028169014 | happy | neutral | That seems steady. I can help with the next step. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.5 | neutral | 0.5 | neutral | 0.62 | neutral | 0.56 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.5 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.4003614457831325 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.5 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6250684931506849 | neutral | neutral | Thanks for sharing. I will keep things straightforward. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.5 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.441578947368421 | sad | neutral | That seems steady. I can help with the next step. |
| 1 | I am really happy with how this turned out. | 0.75 | happy | 0.4262295081967213 | neutral | 0.62 | happy | 0.3396721311475409 | happy | neutral | That sounds genuinely positive. I am glad it is going well. |
| 2 | Today felt rough and I am still sad about it. | 0.75 | sad | 0.4262295081967213 | neutral | 0.62 | sad | 0.3396721311475409 | sad | neutral | That seems hard. We can focus on one small next step. |
| 3 | I am frustrated because the system keeps failing. | 0.75 | angry | 0.4166666666666667 | neutral | 0.62 | neutral | 0.3425 | angry | neutral | Understood. I will stay focused and supportive. |
| 4 | I feel okay, just checking in for now. | 0.75 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.7085714285714285 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 0.75 | fear | 0.396551724137931 | neutral | 0.62 | neutral | 0.3489655172413793 | fear | neutral | This reads as neutral, so I will keep the response practical. |
| 6 | Wow, I did not expect that result at all. | 0.75 | surprise | 0.3396226415094339 | neutral | 0.62 | neutral | 0.3672641509433962 | surprise | neutral | Understood. I will stay focused and supportive. |
| 7 | That smelled gross and made me uncomfortable. | 0.75 | disgust | 0.396551724137931 | neutral | 0.62 | neutral | 0.3489655172413793 | disgust | neutral | That seems steady. I can help with the next step. |
| 8 | I am excited and relieved after finishing the task. | 0.75 | happy | 0.5070422535211268 | neutral | 0.62 | happy | 0.4002816901408451 | happy | neutral | I am picking up an upbeat tone here. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 0.75 | neutral | 0.5 | neutral | 0.62 | neutral | 0.53 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 0.75 | angry | 0.325301204819277 | neutral | 0.62 | neutral | 0.2905421686746987 | angry | neutral | That seems steady. I can help with the next step. |
| 11 | The meeting was fine and nothing unusual happened. | 0.75 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6276027397260274 | neutral | neutral | Thanks for sharing. I will keep things straightforward. |
| 12 | I feel a bit disappointed, but I can recover from it. | 0.75 | sad | 0.3859649122807018 | neutral | 0.62 | neutral | 0.3523684210526315 | sad | neutral | That seems steady. I can help with the next step. |
| 1 | I am really happy with how this turned out. | 1.0 | happy | 0.4262295081967213 | neutral | 0.62 | happy | 0.4262295081967213 | happy | neutral | That sounds genuinely positive. I am glad it is going well. |
| 2 | Today felt rough and I am still sad about it. | 1.0 | sad | 0.4262295081967213 | neutral | 0.62 | sad | 0.4262295081967213 | sad | neutral | That seems hard. We can focus on one small next step. |
| 3 | I am frustrated because the system keeps failing. | 1.0 | angry | 0.4166666666666667 | neutral | 0.62 | angry | 0.4166666666666667 | angry | neutral | I can see frustration here. Let us keep the next step practical. |
| 4 | I feel okay, just checking in for now. | 1.0 | neutral | 0.738095238095238 | neutral | 0.62 | neutral | 0.738095238095238 | neutral | neutral | Understood. I will stay focused and supportive. |
| 5 | I am nervous about the presentation tomorrow. | 1.0 | fear | 0.396551724137931 | neutral | 0.62 | fear | 0.396551724137931 | fear | neutral | That sounds uncertain. Let us break it into a clear next step. |
| 6 | Wow, I did not expect that result at all. | 1.0 | surprise | 0.3396226415094339 | neutral | 0.62 | surprise | 0.3396226415094339 | surprise | neutral | That seems a bit sudden. I can help sort through it. |
| 7 | That smelled gross and made me uncomfortable. | 1.0 | disgust | 0.396551724137931 | neutral | 0.62 | disgust | 0.396551724137931 | disgust | neutral | That feels strongly negative. I can help redirect us. |
| 8 | I am excited and relieved after finishing the task. | 1.0 | happy | 0.5070422535211268 | neutral | 0.62 | happy | 0.5070422535211268 | happy | neutral | I am picking up an upbeat tone here. |
| 9 | It is a mixed day: part of me feels hopeful, part of me feels tired. | 1.0 | neutral | 0.5 | neutral | 0.62 | neutral | 0.5 | neutral | neutral | That seems steady. I can help with the next step. |
| 10 | I am angry, but also a little worried about what comes next. | 1.0 | angry | 0.325301204819277 | neutral | 0.62 | angry | 0.325301204819277 | angry | neutral | That feels frustrating. Let us make it more manageable. |
| 11 | The meeting was fine and nothing unusual happened. | 1.0 | neutral | 0.6301369863013698 | neutral | 0.62 | neutral | 0.6301369863013698 | neutral | neutral | Thanks for sharing. I will keep things straightforward. |
| 12 | I feel a bit disappointed, but I can recover from it. | 1.0 | sad | 0.3859649122807018 | neutral | 0.62 | sad | 0.3859649122807018 | sad | neutral | I am sorry this feels difficult. We can take it one step at a time. |

## Case Study Table
| case_id | user_text | text_top_emotion | face_top_emotion | fused_top_emotion | empathetic_response | case_type |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | I am thrilled with the result and genuinely happy. | happy | happy | happy | Nice, that comes across as encouraging. | Congruent |
| 2 | I feel sad and drained after losing the opportunity. | sad | sad | sad | That sounds heavy, and I appreciate you sharing it. | Congruent |
| 3 | I am frustrated that the system keeps crashing. | angry | angry | angry | That sounds tense, and I will stay concise and helpful. | Congruent |
| 4 | I am nervous about the interview tomorrow. | fear | fear | fear | I can help reduce uncertainty by making the next step concrete. | Congruent |
| 5 | Wow, I did not expect that announcement at all. | surprise | surprise | surprise | That feels unexpected. We can unpack it together. | Congruent |
| 6 | I am thrilled with the result, even though the atmosphere around me feels gloomy. | neutral | sad | neutral | That seems steady. I can help with the next step. | Dissonant |
| 7 | I feel sad and drained after losing the opportunity, even though the people around me seem upbeat. | sad | happy | happy | That sounds genuinely positive. I am glad things are going well. | Dissonant |
| 8 | I am frustrated about the delay, even though everything around me feels calm. | angry | neutral | neutral | That seems steady. I can help with the next step. | Dissonant |
| 9 | I am okay, just checking in and moving through the day. | neutral | neutral | neutral | This reads as neutral, so I will keep the response practical. | Ambiguous |
| 10 | Part of me feels hopeful, part of me feels tired. | neutral | neutral | neutral | That seems steady. I can help with the next step. | Ambiguous |

## Mode Comparison Table
| case_id | user_text | text_top_emotion | face_top_emotion | fused_top_emotion | text_only_response | face_only_response | fused_response | case_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | I am thrilled with the result and genuinely happy. | happy | happy | happy | Nice, that comes across as encouraging. | Nice, that comes across as encouraging. | That sounds genuinely positive. I am glad things are going well. | Congruent |
| 2 | I feel sad and drained after losing the opportunity. | sad | sad | sad | I hear some sadness here. Let us keep this gentle. | I hear some sadness here. Let us keep this gentle. | That sounds heavy, and I appreciate you sharing it. | Congruent |
| 3 | I am frustrated that the system keeps crashing. | angry | angry | angry | That feels frustrating. Let us make it more manageable. | That feels frustrating. Let us make it more manageable. | That sounds tense, and I will stay concise and helpful. | Congruent |
| 4 | I am nervous about the interview tomorrow. | fear | fear | fear | That sounds uncertain. Let us break it into a clear next step. | I can help reduce uncertainty by making the next step concrete. | That seems a little tense, so we can slow down and clarify it. | Congruent |
| 5 | Wow, I did not expect that announcement at all. | surprise | surprise | surprise | That feels unexpected. We can unpack it together. | Interesting. Let us make sense of it calmly. | Interesting. Let us make sense of it calmly. | Congruent |
| 6 | I am thrilled with the result, even though the atmosphere around me feels gloomy. | neutral | sad | neutral | Thanks for sharing. I will keep things straightforward and helpful. | That sounds heavy, and I appreciate you sharing it. | That seems steady. I can help with the next step. | Dissonant |
| 7 | I feel sad and drained after losing the opportunity, even though the people around me seem upbeat. | sad | happy | happy | I am sorry this feels difficult. We can take it one step at a time. | I am picking up an upbeat tone here. | Nice, that comes across as encouraging. | Dissonant |
| 8 | I am frustrated about the delay, even though everything around me feels calm. | angry | neutral | neutral | That sounds tense, and I will stay concise and helpful. | That seems steady. I can help with the next step. | That seems steady. I can help with the next step. | Dissonant |
| 9 | I am okay, just checking in and moving through the day. | neutral | neutral | neutral | Understood. I will stay focused and supportive. | This reads as neutral, so I will keep the response practical. | Understood. I will stay focused and supportive. | Ambiguous |
| 10 | Part of me feels hopeful, part of me feels tired. | neutral | neutral | neutral | Thanks for sharing. I will keep things straightforward and helpful. | That seems steady. I can help with the next step. | Thanks for sharing. I will keep things straightforward and helpful. | Ambiguous |

## Human Evaluation Summary Table
_No rows available yet._
