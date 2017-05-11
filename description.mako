<div>
<% plot = None %>
%if comic.plot is not None:
<% plot = comic.plot.string %>
<% plot = plot.replace('\n', '<br>') %>
%endif
%if plot is not None:
${plot}
%endif
</div>
