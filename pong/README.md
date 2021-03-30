# PONG

Welcome to Pong!

I created an interactive pong game using pygame.  Up to four players are possible, with at most one human player. Usually pong is adversarial, but in my version, the players all cooperate to try to get as many hits as possible. 

Here is a simple version of what one player looks like:

![](figures/1p_demo.mov)

Most parameters can be easily modified, including player board size, ball size, speed, etc:

![](figures/adjusted_parameters.mov)

I also implemented computer players! You can find the cpu logic in `players.py`. Here is a 2-player example:

![](figures/2p_withcpu_example.mov)

This cpu is not too good at pong! You can notice this right away, that the basic strategy of following the ball typically backfires, since it speeds up the ball by the same velocity that the player is traveling at.  If you play by yourself for a bit, you can notice that a better strategy is to position yourself such that you are able to reverse the orthogonal velocity of the ball. So I implemented both strategies. 

* Follower
* Reverser

Here is an example of two reversers cooperating with each other. I even increased the ball speed and rate of random orthogonal velocity shifts:

![](figures/2cpu_reversers.mov)

You can see they control the ball very well! Even with the random bounces I implemented into the physics, they recover any errant shots with ease!


Finally, I was very interested to implement a game of all players and no walls, so I added vertical players and the corresponding CPUs. Here is example of four cpus playing together:

![](figures/4cpu_example.mov)


The do pretty well!

One artifact of having four reversers playing together is that the ball can occasionally slow down to a near stop. This is expected, since the reverser player is always trying to reduce the velocity component along the direction parallel to their own movement.  To make their games more interesting, and to test their abilities, I increased the rate of errant bounces. 




