import type { Article } from "../types";

import goetheExamRegistration from "./goethe-exam-registration";
import germanSimulator from "./german-simulator";
import howToStudyGerman from "./how-to-study-german";

/** Newest first — this is the order the index page and the sitemap use. */
export const articles: Article[] = [germanSimulator, howToStudyGerman, goetheExamRegistration];

export function getArticle(slug: string) {
  return articles.find((a) => a.slug === slug);
}

export function relatedArticles(article: Article) {
  return article.related
    .map((slug) => articles.find((a) => a.slug === slug))
    .filter((a): a is Article => Boolean(a));
}
