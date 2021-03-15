package v1

import (
	"errors"
	"github.com/vsatcloud/mars"
	"project/models"
	"project/util"
)

// @Summary 添加 
// @Tags page
// @Param id query int true id
// @Param created_at query date true created_at
// @Param updated_at query date true updated_at
// @Param deleted_at query date true deleted_at
// @Param username query text true username
// @Param password query text true password
// @Param salt query text true salt
// @Param group query text true group
// @Param real_name query text true real_name
// @Security ApiKeyAuth
// @Router  [post]
func HandlerUsersAdd(c *mars.Context) {
	defer c.ResponseJson()
	var params UsersAddParam
	err := c.BindParams(&params)
	if err != nil {
		c.SystemError(err)
		return
	}


	item := models.users{
        Id:  params.Id,
        CreatedAt:  params.CreatedAt,
        UpdatedAt:  params.UpdatedAt,
        DeletedAt:  params.DeletedAt,
        Username:  params.Username,
        Password:  params.Password,
        Salt:  params.Salt,
        Group:  params.Group,
        RealName:  params.RealName,
        }
	err = models.usersNew(&item)
	if err != nil {
		c.SystemError(err)
		return
	}

	log := models.UserOplog{
		UserID:  userID,
		OpType:  models.OpTypeusers,
		IP:      c.ClientIP(),
		Content: "添加users",
		Request: util.JsonMarshal(params),
	}
	models.UserOplogNew(log)
}
