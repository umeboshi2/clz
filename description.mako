<div>
<% plot = None %>
%if comic.plot is not None:
<% plot = comic.plot.string %>
<% plot = plot.replace('\n', '<br>') %>
%endif
<% year = '' %>
<% genre = 'collectible' %>
<% publisher = 'a reputable publisher' %>
%if comic.publicationdate is not None and comic.publicationdate.displayname is not None:
<% year = comic.publicationdate.displayname.string %>
%endif
%if comic.genre is not None:
<% genre = comic.genre.displayname.string %>
%endif
%if comic.publisher is not None:
<% publisher = comic.publisher.displayname.string %>
%endif
A ${year} ${genre} comic from ${publisher}.<br>
%if plot is not None:
Plot:<br>
${plot}
%endif
</div>
