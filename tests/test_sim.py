from app.sim import equity_vs_random_opponents


def test_equity_smoke():
    hero = ["As","Ad"]
    board = []
    h,v,t,dist = equity_vs_random_opponents(hero, board, 1, 2000)
    assert 0.7 < h < 0.9
