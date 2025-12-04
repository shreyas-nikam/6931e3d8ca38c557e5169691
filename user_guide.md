id: 6931e3d8ca38c557e5169691_user_guide
summary: AI Design and deployment lab 5 - Clone User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Visualizing Random Walks with Streamlit

## Introduction to Random Walks
Duration: 0:05:00

Welcome to this interactive guide on understanding Random Walks using a powerful Streamlit application!

A **Random Walk** is a fundamental concept in mathematics and physics that describes a path consisting of a sequence of random steps. Imagine a tiny ant moving on a line, flipping a coin at each step to decide whether to move left or right. That's a basic random walk!

Random walks are incredibly important because they model a vast array of phenomena in the real world:
*   **Stock prices:** The movement of a stock's price can often be approximated by a random walk.
*   **Particle movement:** How pollen grains move in water (Brownian motion) is a classic example.
*   **Genetics:** Changes in gene frequencies over generations.
*   **Search algorithms:** The path taken by a search algorithm to find a solution.
*   **Game theory:** The path a player takes through a game.

This application provides a visual and interactive way to explore different types of random walks and understand how various parameters influence their behavior. By the end of this codelab, you'll have a clear intuitive grasp of:

*   The basics of a random walk.
*   How bias affects a walk's direction.
*   The impact of "jumps" on the walk's path and final distribution.
*   The difference between individual simulation traces and the overall probability distribution.

Let's dive in and see these fascinating concepts in action!

## Exploring the Basic Random Walk
Duration: 0:07:00

In this step, we'll start with the simplest form: the **Basic Random Walk**. Here, at each step, there's an equal chance of moving left or right.

1.  **Locate the Sidebar:** On the left side of the application, you'll find a sidebar with various controls.
2.  **Select Example:** From the "Select Example" dropdown, choose **"Basic Random Walk"**.
3.  **Default Parameters:**
    *   **Number of Steps:** This controls the length of each individual random walk. A higher number means a longer walk.
    *   **Number of Simulations:** This determines how many independent random walks are generated and visualized. More simulations give a clearer picture of the overall behavior.
    *   **Starting Point:** This sets the initial position of all the random walks.

    <aside class="positive">
    <b>Tip:</b> Try starting with `Number of Steps` around `100` and `Number of Simulations` around `50` to begin.
    </aside>

4.  **Show Simulation Traces:** Make sure the **"Show Simulation Traces"** checkbox is selected. This will plot each individual random walk path.
5.  **Run the Simulation:** Click the **"Run Simulation"** button.

    You will see a plot showing multiple lines. Each line represents one simulated random walk. Notice how they meander around the starting point. They might go far left or far right, but often tend to stay somewhat centered.

6.  **Show Probability Distribution:** Now, check the **"Show Probability Distribution"** checkbox.
7.  **Run the Simulation again.**

    You'll now see a second plot below the traces. This is a histogram representing the final positions of all the random walks. For a basic random walk with many steps, you'll notice that the distribution of final positions tends to cluster around the starting point, resembling a bell curve (a **Normal Distribution**). This is a key insight: while individual paths are random, the collection of many paths reveals a predictable pattern!

    <aside class="positive">
    <b>Experiment:</b>
    *   Increase the `Number of Steps`. What happens to the spread of the final positions?
    *   Increase the `Number of Simulations`. How does this affect the smoothness of the probability distribution?
    *   Change the `Starting Point`. How does this shift both the traces and the distribution?
    </aside>

## Understanding the Biased Random Walk
Duration: 0:08:00

Now let's introduce a twist to our random walk: **Bias**. Imagine our ant is no longer flipping a fair coin; instead, one side of the coin comes up more often.

1.  **Select Example:** From the "Select Example" dropdown, choose **"Biased Random Walk"**.
2.  **Observe New Parameter:** You'll notice a new slider appears: **"Probability of moving right (p)"**.
    *   If `p = 0.5`, it's a fair coin – just like our Basic Random Walk.
    *   If `p > 0.5`, the walk has a tendency to move right.
    *   If `p < 0.5`, the walk has a tendency to move left.

3.  **Set Bias (p > 0.5):** Drag the "Probability of moving right (p)" slider to a value like `0.7` or `0.8`.
4.  **Run the Simulation:** Keep both "Show Simulation Traces" and "Show Probability Distribution" checked.
    *   Observe the **simulation traces**. What do you notice about their general direction compared to the basic random walk? They should now predominantly drift towards the right.
    *   Look at the **probability distribution**. The bell curve should now be shifted to the right, indicating that most of the walks end up further to the right of the starting point. The *mean* of the distribution has shifted.

5.  **Set Bias (p < 0.5):** Now, drag the "Probability of moving right (p)" slider to a value like `0.2` or `0.3`.
6.  **Run the Simulation.**
    *   The traces will now show a general drift to the left.
    *   The probability distribution will be shifted to the left.

    <aside class="negative">
    <b>Warning:</b> A small bias can have a significant impact over many steps. Even a `p` of `0.51` (just 1% more likely to go right) would, over thousands of steps, lead to a strong tendency to end up far to the right. This concept is crucial in financial modeling where even tiny statistical advantages can lead to large returns over time.
    </aside>

## Delving into Random Walk with Jumps
Duration: 0:10:00

This is where things get really interesting! Sometimes, events don't just involve small, incremental steps. They can involve sudden, large changes – **jumps**. Think of a stock price that suddenly drops or surges due to unexpected news, or an animal that usually ambles but occasionally makes a huge leap. This type of walk is often called a **Lévy flight** or a **Jump Process**.

1.  **Select Example:** From the "Select Example" dropdown, choose **"Random Walk with Jumps"**.
2.  **Observe New Parameters:** Two new sliders will appear:
    *   **Jump Probability ($\lambda$):** This controls how often a jump occurs. A higher value means jumps are more frequent. It's the probability of a jump happening at any given step.
    *   **Jump Scale ($\sigma_J$):** This controls the magnitude (size) of the jumps when they do occur. A higher value means the jumps are larger.

3.  **Start Simple:**
    *   Set "Jump Probability ($\lambda$)" to a low value, e.g., `0.01` (1%).
    *   Set "Jump Scale ($\sigma_J$)" to a moderate value, e.g., `5.0`.
    *   Keep "Show Simulation Traces" and "Show Probability Distribution" checked.
    *   Click **"Run Simulation"**.

    You'll notice that most of the time, the walk still looks like a regular random walk, but occasionally, a trace will suddenly make a very large move up or down. These are the "jumps"!

4.  **Increase Jump Probability:** Increase "Jump Probability ($\lambda$)" to a higher value, e.g., `0.1` (10%).
5.  **Run the Simulation.**
    *   Jumps will now be more frequent, making the traces look much more erratic and less smooth.
    *   Crucially, observe the **probability distribution**. It might still look somewhat bell-shaped in the middle, but notice the "tails" – the extreme ends of the distribution. They should be much "fatter" or "heavier" than with a basic random walk. This means there's a higher probability of ending up very far from the starting point compared to a normal distribution. These "fat tails" are a hallmark of jump processes.

6.  **Increase Jump Scale:** Now, keep "Jump Probability ($\lambda$)" around `0.05` and increase "Jump Scale ($\sigma_J$)" to a high value, e.g., `10.0` or `15.0`.
7.  **Run the Simulation.**
    *   You'll see fewer jumps than in the previous step, but when they do happen, they are much larger, causing significant deviations.
    *   The probability distribution's tails will become even more pronounced.

    <aside class="positive">
    <b>Think about it:</b> Why are "fat tails" important? In financial markets, fat tails mean that extreme events (large crashes or surges) are more likely than a simple normal distribution would suggest. This has huge implications for risk management!
    </aside>

## Experimenting and Drawing Conclusions
Duration: 0:05:00

You've now explored the three core types of random walks available in this application. This is your chance to experiment freely and solidify your understanding.

1.  **Play with Parameters:** Go back to each "Select Example" and try different combinations of "Number of Steps", "Number of Simulations", "Starting Point", "Bias", "Jump Probability", and "Jump Scale".
2.  **Observe the Differences:**
    *   How do the individual simulation traces change?
    *   How does the overall probability distribution of final positions change?
    *   What is the relationship between the `Number of Simulations` and the smoothness of the probability distribution? (More simulations generally lead to a smoother, more accurate representation of the underlying theoretical distribution).

    <aside class="positive">
    <b>Challenge:</b> Try to create a "Biased Random Walk" that *looks* like it has jumps by setting a very high bias and a low number of steps. Can you tell the difference by looking at the probability distribution?
    </aside>

**Key Takeaways:**

*   **Basic Random Walk:** Equal chance left/right. Results in a bell-shaped (Normal) probability distribution centered around the starting point for many steps.
*   **Biased Random Walk:** Unequal chance left/right. Shifts the entire distribution in the direction of the bias.
*   **Random Walk with Jumps:** Occasional large movements. Leads to "fat tails" in the probability distribution, meaning extreme events are more likely.
*   **Probability vs. Individual Paths:** While individual random walk paths are unpredictable, the collective behavior of many walks reveals predictable statistical patterns, especially in the final position distribution.

You've successfully navigated the core functionalities of this Streamlit application and gained a deeper understanding of random walks! This conceptual understanding is a valuable tool for anyone interested in modeling dynamic processes in various fields.
