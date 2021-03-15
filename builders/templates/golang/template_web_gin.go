package v1

import (
	"errors"
	"github.com/vsatcloud/mars"
	"project/models"
	"project/util"
)

// @Summary 添加 {{ entity }}
// @Tags page
{% for column in columns -%}
// @Param {{column.name}} query {{column.type}} true {{column.name}}
{% endfor -%}
// @Security ApiKeyAuth
// @Router  [post]
func Handler{{ name | title }}Add(c *mars.Context) {
	defer c.ResponseJson()
	var params {{ name| title }}AddParam
	err := c.BindParams(&params)
	if err != nil {
		c.SystemError(err)
		return
	}


	item := models.{{ name }}{
        {% for column in columns -%}
        {{column.name|word2hump}}:  params.{{column.name|word2hump}},
        {% endfor -%}
	}
	err = models.{{name}}New(&item)
	if err != nil {
		c.SystemError(err)
		return
	}

	log := models.UserOplog{
		UserID:  userID,
		OpType:  models.OpType{{name}},
		IP:      c.ClientIP(),
		Content: "添加{{name}}",
		Request: util.JsonMarshal(params),
	}
	models.UserOplogNew(log)
}

