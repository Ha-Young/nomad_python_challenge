from io import StringIO


def csv_extract(jobs, Response, export_job):
    output = StringIO()
    output.write("Title,Company,URL\n")

    for job in jobs:
        output.write(str(job["title"]) + ',')  # title
        output.write(str(job["company"]) + ',')  # company
        output.write(str(job["url"]))  # company
        output.write("\n")

    response = Response(
        output.getvalue(),
        mimetype="text/csv",
        content_type="application/octet-stream",
    )

    response.headers["Content-Disposition"] = f"attachment; filename={export_job}.csv"

    return response
