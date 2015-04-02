SELECT
  "pgameapp_userprofile"."ref_source",
  "pgameapp_userprofile"."ref_campaign",
  SUM("pgameapp_referralstats"."amount") AS "amount"
FROM
  "pgameapp_userprofile"
INNER JOIN
  "custom_user_emailuser" T3 ON ( "pgameapp_userprofile"."user_id" = T3."id" )
LEFT OUTER JOIN
  "pgameapp_referralstats" ON ( T3."id" = "pgameapp_referralstats"."user_id" )
WHERE
  "pgameapp_userprofile"."referrer_id" = 1
GROUP BY
  "pgameapp_userprofile"."ref_source", "pgameapp_userprofile"."ref_campaign";


SELECT
  "pgameapp_userprofile"."ref_source",
  "pgameapp_userprofile"."ref_campaign",
  SUM("pgameapp_useractorownership"."num_actors") AS "amount"
FROM
  "pgameapp_userprofile"
INNER JOIN
  "custom_user_emailuser" T3 ON ( "pgameapp_userprofile"."user_id" = T3."id" )
LEFT OUTER JOIN
    "pgameapp_useractorownership" ON ( T3."id" = "pgameapp_useractorownership"."user_id" )
WHERE
  "pgameapp_userprofile"."referrer_id" = 1
GROUP BY
  "pgameapp_userprofile"."ref_source", "pgameapp_userprofile"."ref_campaign"