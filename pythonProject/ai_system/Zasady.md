# Zasady na podstawie mierzalnych parametrów
Mierzalne parametry:
1. Kąt - od -179 do 180, zero jako idealna pozycja wertykalna do lądowania.
2. Prędkość:
   - boczna/horyzontalna (deltaX) - od minus nieskończności do nieskończoności, gdzie ujemne wartości do podróż rakiety w lewo, a dodatnie - w prawo.
   - wertykalna (deltaY) - plus/minus nieskończność, gdzie wartości dodatnie do zwrot w dół.
3. Lokalizacja na planszy:
   - na osi X
   - na osi Y
   - odległość od gruntu

# Zasady optymalizacji parametrów

## Kąt
1. Kąt natarcia nie powinien nigdy być większy niż 90 stopni ani mniejszy niż -90 stopni (horyzontalny), bo wówczas rakieta będzie przyspieszać w kierunku gruntu.
2. Przy kątach bliskich horyzontalnemu generalnie powinien być skorygowany w stronę zero.
3. Najlepiej, żeby kąt plasował się w okolicy 0 stopni +/- 30.

## Prędkość
1. Prędkość boczna (delta_x) powinna być poniżej wartości absolutnej z jeden, najlepiej poniżej wartości absolutnej z 0,5.
2. Prędkość wertykalna powinna mieścić się w tych samych zakresach dla wartości dodatnich i nie być ujemna.

## Lokalizacja
1. Im niższa wysokość nad gruntem tym wolniejsza powinna być prędkość i tym kąt powinien być bliższy 0.
2. Rakieta powinna dążyć do ustawiania się w kieurnku centrum planszą.
3. Rakieta powinna mocno odbić jeśli znajduje się poza planszą


# Zasady dla systemów wyjściowych
1. Sytuacja kryzysowa 1: Za wysoka deltaY (prędkość do ziemi zbyt wysoka):
   - jeśli kąt jest bliski zero - zwiększ mocno napęd.
   - jeśli kąt jest dodatni, ale mniejszy od 90 - zwiększ napęd trochę.
   - jeśli kąt jest ujemny, ale wiekszy od -90 - zwiększy napęd trochę.
   - jeśli kąt jest zbyt wysoki najpierw skoryguj kąt natarcia.
2. Sytuacja kryzysowa 2: Niebezpieczny kąt natarcia:
   - jeśil kąt jest 30-90 - zmniejsz go trochę.
   - jeśli kąt jest -30-(-90) - zwiększ go trochę.
   - jeśli kąt jest powyżej 90 - zmniejsz znacznie.
   - jeśli kąt jest poniżej -90 - zwiększ go znacznie.
3. Sytuacja kryzysowa 3: Statek zbyt daleko od środka planszy.
   - jeśli pozycjaX mniejsza niż 100 - statek blisko krawędzi planszy! kąt ujemny i zwiększ moc silnika!
   - jeśli pozycjaX większa niż 900 - statek blisko krawędzi planszy! kąt ujemny i zwiększ moc silnika!
   - jesli posX mniejsza niż 300 i kąt dodatni to zwiększ nieco moc.
   - jeśli poxY większa niż 700 i kąt ujemny to zwiększ nieco moc.
   - #TODO mogłoby działac na wartościach relatywnych!
4. Sytuacja kryzysowa 4: Statek za mocno leci na bok
   - jeśli deltaX jest większa niż 0.5 to zmniejsz kąt.
   - jeśli deltaX jest mniejsza niż -0.5 to zwiększ kąt.
   - jeśli deltaX jest większa niż 0.3 i kąt jest ujemny to zwiększ napęd.
   - jesli deltaX jest mniejsza niż -0.3 i kąt jest dodatni to zwiększ napęd.
5. Sytuacja kryzysowa 5: Statek osiągnął prędkość ucieczkową (y_vel < 0)
   - ogranicz użycie silników aż statek zacznie znowu spadać
   