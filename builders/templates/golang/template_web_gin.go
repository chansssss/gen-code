package v1

import (
	"errors"
	"github.com/vsatcloud/mars"
	"project/models"
	"project/util"
)

// @Summary 添加 {{ name | singular_and_title }}
// @Tags page
{% for column in columns -%}
// @Param {{column.name}} query {{column.type}} true {{column.name}}
{% endfor -%}
// @Security ApiKeyAuth
// @Router  [post]
func Handler{{ name | singular_and_title }}Add(c *mars.Context) {
	defer c.ResponseJson()
	var params {{ name| singular_and_title }}AddParam
	err := c.BindParams(&params)
	if err != nil {
		c.SystemError(err)
		return
	}

// 	判断存在逻辑


	item := models.{{ name | singular_and_title}}{
        {% for column in columns -%}
        {% if column.name != 'id' -%}
        {{column.name|word2hump}}:  params.{{column.name|word2hump}},
        {% endif -%}
        {% endfor -%}
	}
	err = models.{{name | singular_and_title}}New(&item)
	if err != nil {
		c.SystemError(err)
		return
	}

	log := models.UserOplog{
		UserID:  userID,
		OpType:  models.OpType{{name | singular_and_title}},
		IP:      c.ClientIP(),
		Content: "添加{{name | singular_and_title}}",
		Request: util.JsonMarshal(params),
	}
	models.UserOplogNew(log)
}

// @Summary 更新 {{ name | singular_and_title }}
// @Tags page
{% for column in columns -%}
// @Param {{column.name}} query {{column.type}} true {{column.name}}
{% endfor -%}
// @Security ApiKeyAuth
// @Router  [put]
func HandlerPageTMUpdate(c *mars.Context) {
	defer c.ResponseJson()
	var params {{ name| singular_and_title }}UpdateParam
	err := c.BindParams(&params)
	if err != nil {
		c.SystemError(err)
		return
	}

	userID := ContextUserID(c)

	item, err = models.{{ name| singular_and_title }}GetBy{{ name| singular_and_title }}ID(userID, params.ID)
	if err != nil {
		c.SystemError(err)
		return
	}
	if item.ID == 0 {
		c.SystemError(errors.New("记录不存在"))
		return
	}

    {% for column in columns -%}
    {% if column.name != 'id' -%}
    item.{{column.name|word2hump}} = params.{{column.name|word2hump}},
    {% endif -%}
    {% endfor -%}
	err = models.PageTmUpdate(&item)
	if err != nil {
		c.SystemError(err)
		return
	}

	log := models.UserOplog{
		UserID:  userID,
		OpType:  models.OpType{{name | singular_and_title}},
		IP:      c.ClientIP(),
		Content: "更新{{name | singular_and_title}}",
		Request: util.JsonMarshal(params),
	}
	models.UserOplogNew(log)
}

// @Summary 删除 {{ name| singular_and_title }}
// @Tags page
// @Param id query int true "ID"
// @Security ApiKeyAuth
// @Router [delete]
func Handler{{ name| singular_and_title }}Delete(c *mars.Context) {
	defer c.ResponseJson()
	var params {{ name| singular_and_title }}DeleteParam
	err := c.BindParams(&params)
	if err != nil {
		c.SystemError(err)
		return
	}

	userID := ContextUserID(c)
	err = models.{{ name| singular_and_title }}DeleteByID(userID, params.ID)
	if err != nil {
		c.SystemError(err)
		return
	}

	log := models.UserOplog{
		UserID:  userID,
		OpType:  models.OpType{{name | singular_and_title}},
		IP:      c.ClientIP(),
		Content: "删除{{name |  singular_and_title}}",
		Request: util.JsonMarshal(params),
	}
	models.UserOplogNew(log)
}

// @Summary 获取 {{ name| singular_and_title }}
// @Tags page
// @Param id query int false "ID"
// @Param page query int false "页数，默认：1" default(1)
// @Param limit query int false "数量，默认：10" default(10)
// @Security ApiKeyAuth
// @Success 200 {object} {{ name| singular_and_title }}ListData
// @Router  [get]
func Handler{{ name| singular_and_title }}List(c *mars.Context) {
	defer c.ResponseJson()
	var params {{ name| singular_and_title }}ListParam
	err := c.BindParams(&params)
	if err != nil {
		c.SystemError(err)
		return
	}

	userID := ContextUserID(c)
	items, count, err := models.{{ name| singular_and_title }}List(userID, params.ID, params.Page, params.Limit)
	if err != nil {
		c.SystemError(err)
		return
	}

	var data {{ name| singular_and_title }}ListData
	data.Count = count
	data.Items = []{{ name| singular_and_title }}ListItem{}

	for _, i := range items {
		item := {{ name| singular_and_title }}ListItem{
			{% for column in columns -%}
                {{column.name|word2hump}}:  i.{{column.name|word2hump}},
            {% endfor -%}
		}
		data.Items = append(data.Items, item)
	}
	c.SetData(data)

	log := models.UserOplog{
		UserID:  userID,
		OpType:  models.OpType{{name | singular_and_title}},
		IP:      c.ClientIP(),
		Content: "获取{{name | singular_and_title}}列表",
		Request: util.JsonMarshal(params),
	}
	models.UserOplogNew(log)
}

