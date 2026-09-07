/**
 * The API lives on its own host, so it can be down while the site is up.
 * A page that can still say something useful without data uses this to fall
 * back instead of throwing the whole render away.
 */
export const EMPTY_HOME = {
  featured_courses: [],
  newest_courses: [],
  simulators: [],
  frequent_exams: [],
  podcasts: [],
  latest_episodes: [],
  categories: [],
  instructors: [],
  stats: { students: 0, courses: 0, exams: 0, episodes: 0 },
};

export async function orOffline<T>(promise: Promise<T>, fallback: T): Promise<[T, boolean]> {
  try {
    return [await promise, true];
  } catch (caught) {
    console.error("API unreachable:", caught);
    return [fallback, false];
  }
}
