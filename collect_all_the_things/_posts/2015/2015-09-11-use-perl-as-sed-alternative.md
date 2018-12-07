---
layout: default
categories:
- Linux
---
Small tip for people often using sed for substitutions:
In the process of porting my old wordpress blog posts to Jekyll I had to do a lot of substitutions. Specifically I had to substitute a lot of HTML Tags. Sadly, sed in most Linux distributions doesn't support lazy regex quantifiers. When searching for an expression which is only known to begin with **<code** and end with **>** and a lot of possibilites between those delimiters, it's really annoying to not have lazy quantifiers.

That's why I'd recommend using perl for this. Perl can easily be used like sed:

{% highlight bash %}
# sed
sed -e 's/<code.*lang="bash".*>/&#123;% highlight bash %&#125;/g' test.html
# perl
perl -pe 's/<code.*?lang="bash".*?>/&#123;% highlight bash %&#125;/g' test.html
# Of course you can substitute inline:
perl -pi -e 's/<code.*?lang="bash".*?>/&#123;% highlight bash %&#125;/g' test.html
{% endhighlight %}


I really prefer the Regex handling of perl over the limited one of sed. That's why I totally fell in love with this.
