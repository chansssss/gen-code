package v1

type {{ name | singular_and_title }}ListItem struct {
	ID     uint   `json:"id"`
	{% for column in columns -%}
    {% if column.name != 'id' -%}
    {{column.name|word2hump}}  {% if column.type == 'date' -%}int64 {% else %}{{column.type}} {% endif -%} `form:"{{column.name}}" json:"{{column.name}}"`
    {% endif -%}
    {% endfor -%}
}

type {{ name | singular_and_title }}ListData struct {
	Count int64            `json:"count"`
	Items []{{ name | singular_and_title }}ListItem `json:"items"`
}

type {{ name | singular_and_title }}ListParam struct {
	ID     uint `form:"id" json:"id"`
	Page   int  `form:"page" json:"page" default:"1"`
	Limit  int  `form:"limit" json:"limit" default:"10"`
}

type {{ name | singular_and_title }}AddParam struct {
	{% for column in columns -%}
    {% if column.name != 'id' -%}
    {{column.name|word2hump}}  {% if column.type == 'date' -%}int64 {% else %}{{column.type}} {% endif -%} `form:"{{column.name}}" json:"{{column.name}}"`
    {% endif -%}
    {% endfor -%}
}

type {{ name | singular_and_title }}UpdateParam struct {
	ID     uint   `form:"id" json:"id" binding:"required"`
	{% for column in columns -%}
    {% if column.name != 'id' -%}
    {{column.name|word2hump}}  {% if column.type == 'date' -%}int64 {% else %}{{column.type}} {% endif -%} `form:"{{column.name}}" json:"{{column.name}}"`
    {% endif -%}
    {% endfor -%}
}

type {{ name | singular_and_title }}DeleteParam struct {
	ID uint `form:"id" json:"id" binding:"required"`
}
