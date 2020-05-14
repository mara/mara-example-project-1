SELECT review_id,
       order_id,
       review_score,
       trim(regexp_replace(regexp_replace(review_comment_title, E'[\\n\\r]+', ' ', 'g'), ';|\\', '.', 'g')), --remove new lines, trim, and replace ';' and '\' with '.'
       trim(regexp_replace(regexp_replace(review_comment_message, E'[\\n\\r]+', ' ', 'g'), ';|\\', '.', 'g')), --remove new lines, trim, and replace ';' and '\' with '.'
       review_creation_date,
       review_answer_timestamp
FROM ecommerce.order_reviews
WHERE review_creation_date >= to_date('@@first-date@@', 'YYYY-MM-DD')