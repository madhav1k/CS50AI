import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # raise NotImplementedError
    # Initialise probability distribution dictionary:
    prob_distribution = {page_name: 0 for page_name in corpus}
    # If page has no links, return equal probability for the corpus:
    if len(corpus[page]) == 0:
        for page_name in prob_distribution:
            prob_distribution[page_name] = 1 / len(corpus)
        return prob_distribution
    # Probability of picking any page at random:
    random_prob = (1 - damping_factor) / len(corpus)
    # Probability of picking a link from the page:
    link_prob = damping_factor / len(corpus[page])
    # Add probabilities to the distribution:
    for page_name in prob_distribution:
        prob_distribution[page_name] += random_prob
        if page_name in corpus[page]:
            prob_distribution[page_name] += link_prob
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    visits = {page_name: 0 for page_name in corpus}
    # First page choice is picked at random:
    curr_page = random.choice(list(visits))
    visits[curr_page] += 1
    # For remaining n-1 samples, pick the page based on the transistion model:
    for i in range(0, n-1):
        probability_distribution = transition_model(corpus, curr_page, damping_factor)
        # Pick next page based on the transition model probabilities:
        rand_val = random.random()
        total_prob = 0
        for page_name, probability in probability_distribution.items():
            total_prob += probability
            if rand_val <= total_prob:
                curr_page = page_name
                break
        visits[curr_page] += 1
    # Normalise visits using sample number:
    page_ranks = {page_name: (visit_num/n) for page_name, visit_num in visits.items()}
    print('Sum of sample page ranks: ', round(sum(page_ranks.values()), 4))
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    # Calculate some constants from the corpus for further use:
    N = len(corpus)
    initial_rank = 1 / N
    random_choice_probability = (1 - damping_factor) / N
    iterations = 0
    # Initial page_rank gives every page a rank of 1/(num pages in corpus)
    page_ranks = {page_name: initial_rank for page_name in corpus}
    new_ranks = {page_name: None for page_name in corpus}
    max_rank_change = initial_rank
    # Iteratively calculate page rank until no change > 0.001
    while max_rank_change > 0.001:
        iterations += 1
        max_rank_change = 0
        for page_name in corpus:
            surfer_choice_probability = 0
            for other_page in corpus:
                # If other page has no links it picks randomly any corpus page:
                if len(corpus[other_page]) == 0:
                    surfer_choice_probability += page_ranks[other_page] * initial_rank
                # Else if other_page has a link to page_name, it randomly picks from all links on other_page:
                elif page_name in corpus[other_page]:
                    surfer_choice_probability += page_ranks[other_page] / len(corpus[other_page])
            # Calculate new page rank
            new_rank = random_choice_probability + (damping_factor * surfer_choice_probability)
            new_ranks[page_name] = new_rank
        # # Normalise the new page ranks:
        # norm_factor = sum(new_ranks.values())
        # new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}
        # Find max change in page rank:
        for page_name in corpus:
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change
        # Update page ranks to the new ranks:
        page_ranks = new_ranks.copy()
    print('Iteration took', iterations, 'iterations to converge')
    print('Sum of iteration page ranks: ', round(sum(page_ranks.values()), 4))
    return page_ranks


if __name__ == "__main__":
    main()
