; problem 03
(define (problem bw_5_1)
  (:domain blocks-domain)
  (:objects
    b1 b2 b3 b4 b5 - block
  )
  (:init
    (emptyhand)
    (on b1 b3)
    (on b2 b1)
    (on-table b3)
    (on-table b4)
    (on b5 b4)
    (clear b2)
    (clear b5)
  )
  (:goal
    (and (emptyhand) (on b1 b2) (on b2 b5) (on-table b3) (on-table b4) (on-table b5) (clear b1) (clear b3) (clear b4))
  )
)