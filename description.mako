<div>
<% plot = None %>
%if comic.plot is not None:
<% plot = comic.plot.string %>
<% plot = plot.replace('\n', '<br>') %>
%endif
A ${comic.publicationdate.displayname.string} ${comic.genre.displayname.string} comic from ${comic.publisher.displayname.string}.<br>
%if plot is not None:
Plot:<br>
${plot}
%endif
</div>
