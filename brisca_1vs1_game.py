
from environments.human_oponent_env import HumanOponentEnvironment
from func_approx import FunctApproxMethodology
from environments.brisca_env import State
import click

@click.command()
@click.option('--l', default=1, help='lambda value for the sarsa control: 0 = sarsa, 1 = monte-carlo')
def main(l):
    environment = HumanOponentEnvironment()
    method = FunctApproxMethodology('weights/Same_Policy_weights.npy')

    rl_agent_hand = environment.get_starting_hand()
    st = State(
            rl_agent_hand, 
            environment.ruling_suit, 
            environment.cards_in_play[0] if len(environment.cards_in_play) > 0 else None
    )
    act = method.select_action(st)
    while not environment.is_game_finished(st.hand, environment.oponent_hand):
        #take action and observe Reward and New state
        st_, reward = environment.step(st, act, method)
        
        #choose new action from derived new state
        if not environment.is_game_finished(st_.hand, environment.oponent_hand):
            act_ = method.select_action(st_)
            delta = (1 - l) * method.get_q_hat(st_, act_) - method.get_q_hat(st, act)
            method.theta += method.get_alpha() * (reward + delta) * method.get_feature_vector(st, act)
            act = act_
        else:
            method.theta += method.get_alpha() * (reward - method.get_q_hat(st, act)) * method.get_feature_vector(st, act)
            act = None
        st = st_

    print(environment.points)

if __name__ == '__main__':
    main()